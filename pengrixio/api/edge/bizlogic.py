import ast
import uuid
import etcd
import json
import requests

import logging
import logging.config

from datetime import datetime

from pengrixio.database import etcdc
from pengrixio.k8s.node import kube_list_node
from pengrixio.k8s.pod import kube_list_pod
from pengrixio.k8s.namespace import kube_list_namespace
from pengrixio.k8s.namespace import kube_create_namespace
from pengrixio.k8s.namespace import kube_delete_namespace
from pengrixio.api.tenant.bizlogic import get_tenant


from pengrixio.config import PROJECT_ROOT
from pengrixio.k8s.utils import cmd

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

def get_edge(name=None):
    """Get edge list.
    """
    l_edge = list()
    if name is None:
        s_rsc = '{}/edge'.format(etcdc.prefix)
    else:
        s_rsc = '{}/edge/{}'.format(etcdc.prefix, name)

    try:
        r = etcdc.read(s_rsc, recursive=True, sorted=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
    else:
        for child in r.children:
            d = ast.literal_eval(child.value)
            l_hosts = kube_list_node(PROJECT_ROOT + '/' + d['endpoint'])
            d['hosts'] = len(l_hosts)
            #l_pods = kube_list_pod()
            #d['pods'] = len(l_pods)
            # get # of tenants and apps
            l_tenants = get_tenant(d['name'])
            log.debug(l_tenants)
            d['tenants'] = len(l_tenants)
            d['apps'] = 0
            for e in l_tenants:
                d['apps'] += len(e['app'])

            d['cpu'] = 0
            d['memory'] = 0
            i_total_cores = 0
            i_total_memory = 0
            i_total_storage = 0
            for h in l_hosts:
                i_total_cores += int(h.status.capacity['cpu'])
                i_total_memory += int(h.status.capacity['memory'].
                        replace('Ki', ''))
            d['tot_cpu'] = i_total_cores
            d['tot_mem'] = int(i_total_memory / (1024*1024))
            # Get loadavg and free mem
            if d['name'] == 'edge1':
                ssh_server = 'harden.iorchard.co.kr'
            elif d['name'] == 'edge2':
                ssh_server = 'durant.iorchard.co.kr'
            RSC = 'ssh -p42544 {} get_rsc.sh'.format(ssh_server)
            log.debug(RSC)
            (b_res, s_out) = cmd(RSC, 3, False)
            l = s_out.split("\n")
            log.debug(l)
            d['used_cpu'] = (float(l[0]) + float(l[1]) + float(l[2]))
            avail_mem = (int(l[3]) + int(l[4]) + int(l[5])) / (1024*1024)
            d['used_mem'] = d['tot_mem'] - avail_mem
            log.debug(d['used_mem'])
            d['cpu'] = int(d['used_cpu'] / d['tot_cpu'] * 100)
            d['memory'] = int(d['used_mem'] / d['tot_mem'] * 100)
            # ceph storage
            CEPH = "kubectl --kubeconfig " + PROJECT_ROOT + '/' \
                    + d['endpoint'] + " -n rook-ceph exec -it " \
                    + "$(kubectl --kubeconfig " + PROJECT_ROOT + '/' \
                    + d['endpoint'] + " -n rook-ceph get po " \
                    + "-l app=rook-ceph-tools " \
                    + "-o jsonpath='{.items[0].metadata.name}') -- " \
                    + "ceph df --format json"
            log.debug(CEPH)
            (b_res, s_out) = cmd(CEPH, 3, False)
            d['status'] = 'Healthy' if b_res else 'Unhealthy'
            d_stor = ast.literal_eval(s_out)
            d['tot_stor'] = int(d_stor['stats']['total_bytes'] / pow(1024, 3))
            d['used_stor'] = int(d_stor['stats']['total_used_bytes'] / pow(1024, 3))
            d['storage'] = int(d['used_stor'] / d['tot_stor'] * 100)

            l_edge.append(d)
    finally:
        return l_edge

def create_edge(data):
    """Create edge
    edgePostSerializer
    """
    if not data.get('name'):
        return (False, 'Edge name should be specified.')

    t_ret = (False, '')

    s_uuid = str(uuid.uuid4())
    s_created = datetime.utcnow().isoformat() + 'Z'

    data['createdAt'] = s_created
    data['uid'] = s_uuid

    log.debug(data)
    s_rsc = '{}/edge/{}'.format(etcdc.prefix, data['name'])
    try:
        etcdc.write(s_rsc, data, prevExist=False)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'etcd {} is created.'.format(data['name']))
    finally:
        return t_ret

def delete_edge(name):
    """Delete edge.
    """
    if not name:  # <name> should be specified.
        return (False, 'Edge name should be specified.')
        
    t_ret = (False, '')

    s_rsc = '{}/edge/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.delete(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'edge {} is deleted.'.format(name))
    finally:
        return t_ret

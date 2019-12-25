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
            l_edge.append(d)
    finally:
        return l_edge

def get_edge_info(name):
    """Get edge list.
    """
    t_ret = (False, '')
    if not name:  # <name> should be specified.
        return (False, 'Edge name should be specified.')

    d = dict()
    s_rsc = '{}/edge/{}'.format(etcdc.prefix, name)

    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return (False, e)
    else:
        d = ast.literal_eval(r.value)
        t_ret = (True, d)
    finally:
        return t_ret

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

def update_edge(name, data):
    """Update edge
    edgePatchSerializer
    """
    t_ret = (False, '')
    if not name:  # <name> should be specified.
        return t_ret
        
    data = dict((k, v) for k, v in data.items() if v)
    s_rsc = '{}/edge/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
        return t_ret

    d = ast.literal_eval(r.value)

    s_modified = datetime.utcnow().isoformat() + 'Z'
    data['modifiedAt'] = s_modified
    d.update(data.items())

    log.debug(d)
    s_rsc = '{}/edge/{}'.format(etcdc.prefix, name)
    try:
        etcdc.write(s_rsc, d, prevExist=True)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'etcd {} is created.'.format(name))
    finally:
        return t_ret


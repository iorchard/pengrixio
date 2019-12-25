import ast
import time
import etcd
import click

import logging
import logging.config

from flask import Flask
from flask.cli import FlaskGroup
from flask import render_template
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pengrixio.database import etcdc
from pengrixio.k8s.node import kube_list_node
from pengrixio.k8s.pod import kube_list_pod
from pengrixio.api.tenant.bizlogic import get_tenant
from pengrixio.config import PROJECT_ROOT
from pengrixio.config import APP_ROOT

from pengrixio.k8s.utils import cmd
from pengrixio.config import GUAC_USER, GUAC_PASS

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

env = Environment(
    loader=FileSystemLoader(APP_ROOT + '/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def create_app():
    app = Flask('pengmon')
    return app

@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for collector."""
    while True:
        try:
            # Get the whole information on each edge.
            l_edge = list()
            s_rsc = '{}/edge'.format(etcdc.prefix)
    
            try:
                r = etcdc.read(s_rsc, recursive=True)
            except etcd.EtcdKeyNotFound as e:
                log.error(e)
            else:
                for child in r.children:
                    l_app = list()
                    d = ast.literal_eval(child.value)
                    # get hosts
                    print(PROJECT_ROOT + '/' + d['endpoint'])
                    l_hosts = kube_list_node(PROJECT_ROOT + '/' + d['endpoint'])
                    d['hosts'] = len(l_hosts)
                    d_nodes = dict()  # {'name': 'ip', ...}
                    for item in l_hosts:
                        d_nodes[item.metadata.name] = item.status.addresses[0].address
                    # log.debug(d_nodes)
                    # get # of tenants and apps
                    l_tenants = get_tenant(d['name'])
                    d['tenants'] = len(l_tenants)
                    d['apps'] = 0
                    for e in l_tenants:
                        if 'app' in e:
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
                    (b_res, s_out) = cmd(RSC, 3, False)
                    l = s_out.split("\n")
                    d['used_cpu'] = (float(l[0]) + float(l[1]) + float(l[2]))
                    avail_mem = (int(l[3]) + int(l[4]) + int(l[5])) / (1024*1024)
                    d['used_mem'] = d['tot_mem'] - avail_mem
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
                    (b_res, s_out) = cmd(CEPH, 3, False)
                    print(s_out)
                    d['status'] = 'Healthy' if b_res else 'Unhealthy'
                    d_stor = ast.literal_eval(s_out)
                    d['tot_stor'] = int(d_stor['stats']['total_bytes'] / pow(1024, 3))
                    d['used_stor'] = int(d_stor['stats']['total_used_bytes'] / pow(1024, 3))
                    d['storage'] = int(d['used_stor'] / d['tot_stor'] * 100)
                    # Update etcd status
                    try:
                        s = '{}/edge/{}'.format(etcdc.prefix,
                                d['name'])
                        # log.debug(d)
                        etcdc.write(s, d, prevExist=True)
                    except etcd.EtcdKeyNotFound as e:
                        log.error(e)
    
                    # Update app status
                    s_app = '{}/app'.format(etcdc.prefix)
                    try:
                        r_app = etcdc.read(s_app, recursive=True)
                    except etcd.EtcdKeyNotFound as e:
                        log.error(e)
                    else:
                        for app_child in r_app.children:
                            if app_child.value is not None:
                                d_app = dict()
                                app = ast.literal_eval(app_child.value)
                                if app['edge'] == d['name']:
                                    d_app['name'] = app['name']
                                    d_app['username'] = GUAC_USER
                                    d_app['password'] = GUAC_PASS
                                # Get catalog info.
                                s_cat = '{}/catalog/{}'.format(etcdc.prefix,
                                        app['catalog'])
                                try:
                                    r_cat = etcdc.read(s_cat)
                                except etcd.EtcdKeyNotFound as e:
                                    log.error(e)
                                else:
                                    cat = ast.literal_eval(r_cat.value)
                                    app['cat_type'] = cat['type']
                                    app['cat_name'] = cat['name']
                                    app['cat_logo'] = cat['logo']
                                # Get app status
                                if app['cat_type'] == 'vm':
                                    # first, look at DataVolume status of app.
                                    CMD = "kubectl --kubeconfig " + PROJECT_ROOT + '/' \
                                        + d['endpoint'] + ' get dv ' \
                                        + app['name'] \
                                        + " -o jsonpath='{range .status}{.phase},{.progress}{end}'"
                                    (b_res, s_out) = cmd(CMD, 5, False)
                                    l_out = s_out.split(',')
                                    if l_out[0] == 'Succeeded':
                                        # Get vm status of app
                                        CMD = "kubectl --kubeconfig " + PROJECT_ROOT \
                                        + '/' \
                                        + d['endpoint'] + ' get vm ' \
                                        + app['name'] \
                                        + " -o jsonpath='{.status.ready}'"
                                        (b_res, s_out) = cmd(CMD, 5, False)
                                        if b_res and s_out == 'true':
                                            # update app status 'running'.
                                            app.update({'status': 'running'})
        
                                            if app['edge'] == d['name']:
                                                # Get where app is running.
                                                CMD = "kubectl --kubeconfig " \
                                                + PROJECT_ROOT + '/' \
                                                + d['endpoint'] + ' get vmi ' \
                                                + app['name'] \
                                                + " -o jsonpath='{.status.nodeName}'"
                                                (b_res, s_out) = cmd(CMD, 5, False)
                                                if b_res:
                                                    d_app['hostname'] = d_nodes[s_out]
                                                # Get nodeport for app.
                                                CMD = "kubectl --kubeconfig " \
                                                + PROJECT_ROOT + '/' \
                                                + d['endpoint'] + ' get svc ' \
                                                + app['name'] \
                                                + " -o jsonpath='{.spec.ports[0].nodePort}'"
                                                (b_res, s_out) = cmd(CMD, 5, False)
                                                if b_res:
                                                    d_app['port'] = s_out
                                        else:
                                            # update app status 'stopped'
                                            app.update({'status': 'stopped'})
                                    elif l_out[0] == 'ImportInProgress':
                                        # update app status 'building' and 
                                        app.update({'status': 'building ({})'.format(l_out[1])})
                                elif app['cat_type'] == 'container':
                                    app.update({'status': 'running'})
    
                                try:
                                    s = '{}/app/{}'.format(etcdc.prefix,
                                            app['name'])
                                    # log.debug(app)
                                    etcdc.write(s, app, prevExist=True)
                                except etcd.EtcdKeyNotFound as e:
                                    log.error(e)
    
                                if 'port' in d_app:
                                    l_app.append(d_app)
                        # render guac-config.j2 and copy it to guac broker server
                        log.debug(l_app)
                        template = env.get_template('broker.j2')
                        s_out = template.render(l_app=l_app)
                        s_tmp = '/tmp/{}.broker'.format(d['name'])
                        try:
                            with open(s_tmp, 'w') as f:
                                f.write(s_out)
                        except Exception as e:
                            log.error(e)
                        else:
                            CMD = "scp " \
                            + "-P42544 {} {}".format(s_tmp, d['broker_ip']) \
                            + ":/etc/guacamole/noauth-config.xml"
                            log.debug(CMD)
                            (b_res, s_out) = cmd(CMD, 5, False)
                            if b_res:
                                d_app['port'] = s_out
    
                    l_edge.append(d)
    
            # log.debug(l_edge)
            log.debug(l_app)
    
            time.sleep(1)
        except:
            log.error('unknown error')

import ast
import uuid
import etcd
import json
import random
import string
import requests

import logging
import logging.config

from datetime import datetime
from subprocess import Popen

from flask import render_template

from pengrixio.database import etcdc
from pengrixio.config import KUBEMANIFEST
from pengrixio.config import KUBECTL
from pengrixio.config import PROJECT_ROOT

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

def get_app(name=None):
    """Get app list.
    """
    l_app = list()
    if name is None:
        s_rsc = '{}/app'.format(etcdc.prefix)
    else:
        s_rsc = '{}/app/{}'.format(etcdc.prefix, name)

    try:
        r = etcdc.read(s_rsc, recursive=True, sorted=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
    else:
        for child in r.children:
            if child.value is not None:
                d = ast.literal_eval(child.value)
                l_app.append(d)
    finally:
        return l_app

def create_app(data):
    """Create app
    appPostSerializer
    """
    if not data.get('name'):
        return (False, 'App name should be specified.')

    t_ret = (False, '')

    s_uuid = str(uuid.uuid4())
    s_created = datetime.utcnow().isoformat() + 'Z'

    data['createdAt'] = s_created
    data['uid'] = s_uuid

    # Get catalog information from data['catalog']
    s_catalog_rsc = '{}/catalog/{}'.format(etcdc.prefix, data['catalog'])
    try:
        r = etcdc.read(s_catalog_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return t_ret
    else:
        if r.value is not None:
            d = ast.literal_eval(r.value)
            log.debug(d)
            data['cpu_spec'] = d['cpu_spec']
            data['mem_spec'] = d['mem_spec']
            data['disk_spec'] = d['disk_spec'] + 1
            data['image_url'] = d['image_url']

    # Get tenant from data['user']
    s_user_rsc = '{}/account/{}'.format(etcdc.prefix, data['user'])
    try:
        r = etcdc.read(s_user_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return t_ret
    else:
        if r.value is not None:
            d = ast.literal_eval(r.value)
            log.debug(d)
            data['tenant'] = d['tenant']

    # Get edge from tenant
    s_tenant_rsc = '/{}/tenant/{}'.format(etcdc.prefix, d['tenant'])
    try:
        r = etcdc.read(s_tenant_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return t_ret
    else:
        if r.value is not None:
            d = ast.literal_eval(r.value)
            log.debug(d)
            data['edge'] = d['edge']

    s_kubeconfig = PROJECT_ROOT + '/.' + data['edge']

    # Create VM image == app name <username>-<catalog>-<4_random_strings>
    # create vm manifest
    s_out = render_template('vm.j2', d=data)
    s_tpl = '{}/{}_vm.yaml'.format(KUBEMANIFEST, data['name'])
    try:
        with open(s_tpl, 'w') as f:
            f.write(s_out)
    except Exception as e:
        log.error(e)
        return (False, 'Cannot create a manifest file - {}.'.format(s_tpl))
    else:
        # Run kubectl apply
        s_cmd = '{} --kubeconfig={} '.format(KUBECTL, s_kubeconfig) + \
                'apply -f {}'.format(s_tpl)
        Popen(s_cmd, shell=True)

    # create vm service manifest
    s_out = render_template('svc.j2', d=data)
    s_tpl = '{}/{}_svc.yaml'.format(KUBEMANIFEST, data['name'])
    try:
        with open(s_tpl, 'w') as f:
            f.write(s_out)
    except Exception as e:
        log.error(e)
        return (False, 'Cannot create a manifest file - {}.'.format(s_tpl))
    else:
        # Run kubectl apply
        s_cmd = '{} --kubeconfig={} '.format(KUBECTL, s_kubeconfig) + \
                'apply -f {}'.format(s_tpl)
        Popen(s_cmd, shell=True)

    s_rsc = '{}/app/{}'.format(etcdc.prefix, data['name'])
    try:
        etcdc.write(s_rsc, data, prevExist=False)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'App {} is created.'.format(data['name']))
    finally:
        return t_ret

def delete_app(name):
    """Delete app.
    """
    if not name:  # <name> should be specified.
        return (False, 'App name should be specified.')
        
    t_ret = (False, '')

    s_rsc = '{}/app/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.delete(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'app {} is deleted.'.format(name))
    finally:
        return t_ret

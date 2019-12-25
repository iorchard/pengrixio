import ast
import uuid
import etcd
import json
import requests

import logging
import logging.config

from datetime import datetime

from pengrixio.database import etcdc

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

def get_tenant(edge_name=None, name=None):
    """Get tenant list.
    """
    l_tenant = list()
    if name is None:
        s_rsc = '{}/tenant'.format(etcdc.prefix)
    else:
        s_rsc = '{}/tenant/{}'.format(etcdc.prefix, name)

    try:
        r = etcdc.read(s_rsc, recursive=True, sorted=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
    else:
        for child in r.children:
            if child.value is not None:
                d = ast.literal_eval(child.value)
                if edge_name is None:
                    l_tenant.append(d)
                else:
                    if d['edge'] == edge_name:
                        # Get app list for the tenant
                        app_rsc = '{}/app'.format(etcdc.prefix)
                        try:
                            app_r = etcdc.read(app_rsc, recursive=True)
                        except etcd.EtcdKeyNotFound as e:
                            log.error(e)
                        else:
                            d['app'] = list()
                            for child in app_r.children:
                                if child.value is not None:
                                    app = ast.literal_eval(child.value)
                                    if d['name'] == app['tenant']:
                                        d_tmp = {'name': app['name'],
                                                'logo': app['cat_logo'],
                                                'type': app['cat_type'],
                                                'user': app['user'],
                                                'status': app['status'],
                                                'desc': app['desc']
                                                }
                                        d['app'].append(d_tmp)
                            d['app'] = sorted(d['app'], key=lambda k:k['name'])    
                            l_tenant.append(d)
    finally:
        return l_tenant

def get_tenant_info(name):
    """Get tenant info
    """
    d_tenant = dict()
    if name is None:
        return (False, 'tenant name should be specified.')

    s_rsc = '{}/tenant/{}'.format(etcdc.prefix, name)

    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
    else:
        d_tenant = ast.literal_eval(r.value)
    finally:
        return (True, d_tenant)

def create_tenant(data):
    """Create tenant
    tenantPostSerializer
    """
    if not data.get('name'):
        return (False, 'Tenant name should be specified.')

    t_ret = (False, '')

    s_uuid = str(uuid.uuid4())
    s_created = datetime.utcnow().isoformat() + 'Z'

    data['createdAt'] = s_created
    data['uid'] = s_uuid

    # log.debug(data)
    s_rsc = '{}/tenant/{}'.format(etcdc.prefix, data['name'])
    try:
        etcdc.write(s_rsc, data, prevExist=False)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'etcd {} is created.'.format(data['name']))
    finally:
        return t_ret

def delete_tenant(name):
    """Delete tenant.
    """
    if not name:  # <name> should be specified.
        return (False, 'Tenant name should be specified.')
        
    t_ret = (False, '')

    s_rsc = '{}/tenant/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.delete(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'tenant {} is deleted.'.format(name))
    finally:
        return t_ret

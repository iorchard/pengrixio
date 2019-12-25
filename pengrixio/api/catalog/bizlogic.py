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
log = logging.getLogger('pengrixio')

def get_catalog(name=None):
    """Get catalog list.
    """
    l_catalog = list()
    if name is None:
        s_rsc = '{}/catalog'.format(etcdc.prefix)
    else:
        s_rsc = '{}/catalog/{}'.format(etcdc.prefix, name)

    try:
        r = etcdc.read(s_rsc, recursive=True, sorted=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
    else:
        for child in r.children:
            if child.value is not None:
                d = ast.literal_eval(child.value)
                l_catalog.append(d)
    finally:
        return l_catalog

def create_catalog(data):
    """Create catalog
    catalogPostSerializer
    """
    if not data.get('name'):
        return (False, 'Catalog name should be specified.')

    t_ret = (False, '')

    s_uuid = str(uuid.uuid4())
    s_created = datetime.utcnow().isoformat() + 'Z'

    data['createdAt'] = s_created
    data['uid'] = s_uuid

    log.debug(data)
    s_rsc = '{}/catalog/{}'.format(etcdc.prefix, data['name'])
    try:
        etcdc.write(s_rsc, data, prevExist=False)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'etcd {} is created.'.format(data['name']))
    finally:
        return t_ret

def delete_catalog(name):
    """Delete catalog.
    """
    if not name:  # <name> should be specified.
        return (False, 'Catalog name should be specified.')
        
    t_ret = (False, '')

    s_rsc = '{}/catalog/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.delete(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'catalog {} is deleted.'.format(name))
    finally:
        return t_ret


def update_catalog(name, data):
    """Update catalog
    catalogPatchSerializer
    """
    data = dict((k, v) for k, v in data.items() if v)
    t_ret = (False, '')
    if not name:
        return t_ret

    s_rsc = '{}/catalog/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
        return t_ret

    d = ast.literal_eval(r.value)

    data['modifiedAt'] = datetime.utcnow().isoformat() + 'Z'
    d.update(data.items())

    try:
        etcdc.write(s_rsc, d, prevExist=True)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'catalog {} is updated.'.format(name))
    finally:
        return t_ret


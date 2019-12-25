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

def get_dashboard(name=None):
    """Get dashboard information
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


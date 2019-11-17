import kubernetes.client

import logging
import logging.config

from kubernetes.client.rest import ApiException

from pengrixio.config import KUBECTL
from pengrixio.config import KUBEMANIFEST
from pengrixio.config import KUBECONFIG

from pengrixio.k8s.utils import cmd

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')


def kube_list_node(s_config=KUBECONFIG, field_selector='', label_selector=''):
    """Get nodes"""
    try:
        kubernetes.config.load_kube_config(s_config)
    except:
        log.warn('kubernetes cluster config file is invalid.')

    o_api = kubernetes.client.CoreV1Api()

    try:
        o_res = o_api.list_node(
                    field_selector=field_selector,
                    label_selector=label_selector
                )
    except ApiException as e:
        log.error(e)
        s_msg = 'Cannot get node list'
        return []
    else:
        return o_res.items


def kube_read_node(name):
    """Read the specified node"""
    o_api = kubernetes.client.CoreV1Api()

    try:
        o_res = o_api.read_node(name)
    except ApiException as e:
        log.error(e)
        s_msg = 'Cannot get node resource.'
        return {}
    else:
        return o_res

def kube_node_label(name, d_label):
    """Set labels of node."""
    pass

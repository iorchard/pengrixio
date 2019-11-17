import kubernetes.client

import logging
import logging.config

from kubernetes.client.rest import ApiException

from pengrixio.config import KUBECTL
from pengrixio.config import KUBEMANIFEST

from pengrixio.k8s.utils import cmd

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')


o_api = kubernetes.client.CoreV1Api()


def kube_list_namespace(field_selector='', label_selector=''):
    """Get namespaces"""
    try:
        o_res = o_api.list_namespace(
                    field_selector=field_selector,
                    label_selector=label_selector
                )
    except ApiException as e:
        log.error(e)
        return []
    else:
        return o_res.items

def kube_create_namespace(name):
    """Create namespace."""
    body = kubernetes.client.V1Namespace()
    body.metadata = kubernetes.client.V1ObjectMeta(name="{}".format(name))
    try:
        o_res = o_api.create_namespace(body)
    except ApiException as e:
        log.error(e)
        return False
    else:
        return True

def kube_delete_namespace(name):
    """Delete namespace."""
    try:
        o_res = o_api.delete_namespace(
                    name="{}".format(name),
                    body=kubernetes.client.V1DeleteOptions()
                )
    except ApiException as e:
        log.error(e)
        return {}
    else:
        # log.debug(o_res)
        return o_res


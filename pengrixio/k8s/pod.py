import kubernetes.client

import logging
import logging.config

from kubernetes.client.rest import ApiException

from pengrixio.config import KUBECTL
from pengrixio.config import KUBEMANIFEST

from pengrixio.k8s.utils import cmd

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')


def kube_list_pod(namespace=None, field_selector='', label_selector=''):
    """Get pods"""
    o_api = kubernetes.client.CoreV1Api()

    try:
        if namespace:
            o_res = o_api.list_namespaced_pod(
                        namespace,
                        field_selector=field_selector,
                        label_selector=label_selector
                    )
        else:
            o_res = o_api.list_pod_for_all_namespaces(
                        field_selector=field_selector,
                        label_selector=label_selector
                    )
    except ApiException as e:
        log.error(e)
        return []
    except ValueError as e:
        # log.error(e)
        return []
    else:
        return o_res.items

def kube_read_pod(name, namespace):
    """Get pod info"""
    o_api = kubernetes.client.CoreV1Api()

    try:
        o_res = o_api.read_namespaced_pod(
                    name,
                    namespace,
                )
    except ApiException as e:
        log.error(e)
        return {}
    except ValueError as e:
        # log.error(e)
        return {}
    else:
        return o_res


import kubernetes.client

import logging
import logging.config

from kubernetes.client.rest import ApiException

from pengrixio.config import KUBECTL
from pengrixio.config import KUBECONFIG
from pengrixio.config import KUBEMANIFEST

from pengrixio.k8s.utils import cmd

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')


def kube_deploy_list(namespace=None, field_selector='', label_selector=''):
    """Get deployment names"""
    o_api = kubernetes.client.ExtensionsV1beta1Api()

    try:
        if namespace:
            o_res = o_api.list_namespaced_deployment(
                        namespace,
                        field_selector=field_selector,
                        label_selector=label_selector
                    )
        else:
            o_res = o_api.list_deployment_for_all_namespaces(
                        field_selector=field_selector,
                        label_selector=label_selector
                    )
    except ApiException as e:
        log.error(e)
        s_msg = 'Cannot get deployment list'
        return []
    else:
        return o_res.items

def kube_deploy_read(name, namespace):
    """Read the specified deployment"""
    o_api = kubernetes.client.ExtensionsV1beta1Api()

    try:
        o_res = o_api.read_namespaced_deployment(
                        name,
                        namespace
                    )
    except ApiException as e:
        log.error(e)
        s_msg = 'Cannot get deployment resource.'
        return {}
    else:
        return o_res

def kube_deploy_run(s_op='apply', d_app={}):
    """Run deployment resource using manifest file."""
    # create manifest file from d_app.
    if not d_app.get('manifest'):
        s_msg = 'manifest is not defined.'
        return (False, s_msg)
    # Create manifest file.
    s_file = KUBEMANIFEST + '/{}.yml'.format(d_app['name'])
    try:
        with open(s_file, 'w') as f:
            f.write(d_app['manifest'])
    except:
        s_msg = 'Cannot write manifest file {}'.format(s_file)
        return (False, s_msg)

    s_cmd= "{} --kubeconfig {} {} -f {} --record".format(KUBECTL, KUBECONFIG, \
                                                s_op, s_file)
    log.debug(s_cmd)
    (b_ret, l_out) = cmd(s_cmd)

    if not b_ret:
        log.error(l_out)
        s_msg = 'Fail to run App {}'.format(d_app['name'])
        return (b_ret, s_msg)

    s_msg = 'Succeed to run App {}'.format(d_app['name'])
    return (b_ret, s_msg)

def kube_deploy_delete(name='', namespace='default'):
    """Delete deployment resource."""
    if not name:
        s_msg = 'name is not defined.'
        return (False, s_msg)

    # delete deploy and svc
    s_cmd= "{} --kubeconfig {} delete deploy/{} -n {}".format( \
                KUBECTL, KUBECONFIG, name, namespace)
    log.debug(s_cmd)
    (b_ret, l_out) = cmd(s_cmd)

    if not b_ret:
        log.error(l_out)
        s_msg = 'Fail to delete App deploy {}'.format(name)
        return (b_ret, s_msg)

    s_cmd= "{} --kubeconfig {} delete svc/{} -n {}".format( \
                KUBECTL, KUBECONFIG, name, namespace)
    log.debug(s_cmd)
    (b_ret, l_out) = cmd(s_cmd)

    if not b_ret:
        log.error(l_out)
        s_msg = 'Fail to delete App service {}'.format(name)
        return (b_ret, s_msg)

    s_msg = 'Succeed to delete App {}'.format(name)
    return (b_ret, s_msg)

def kube_deploy_scale(name, namespace, replicas):
    """Scale deployment resource."""
    if not name:
        s_msg = 'name is not defined.'
        return (False, s_msg)
    if not namespace:
        s_msg = 'namespace is not defined.'
        return (False, s_msg)
    if not replicas:
        s_msg = 'replicas is not defined.'
        return (False, s_msg)

    # scale deploy
    s_cmd= "{} --kubeconfig {} scale deploy/{} -n {} --replicas {}".format( \
                KUBECTL, KUBECONFIG, name, namespace, replicas)
    log.debug(s_cmd)
    (b_ret, l_out) = cmd(s_cmd)

    if not b_ret:
        log.error(l_out)
        s_msg = 'Fail to scale App {}'.format(name)
        return (b_ret, s_msg)

    s_msg = 'Succeed to scale App {}'.format(name)
    return (b_ret, s_msg)

def kube_deploy_rollingupdate(name, namespace, d_app):
    """Rolling-update deployment resource."""
    if not name:
        s_msg = 'name is not defined.'
        return (False, s_msg)
    if not namespace:
        s_msg = 'namespace is not defined.'
        return (False, s_msg)
    if not d_app:
        s_msg = 'app data is not defined.'
        return (False, s_msg)

    # rolling update deploy using kubectl set
    s_cmd= "{} --kubeconfig {} set image deploy/{} -n {} {}={}:{}".format( \
            KUBECTL, KUBECONFIG, name, namespace, \
            d_app['name'], d_app['image'], d_app['tag'])
    log.debug(s_cmd)
    (b_ret, l_out) = cmd(s_cmd)

    if not b_ret:
        log.error(l_out)
        s_msg = 'Fail to rolling-update App {}'.format(name)
        return (b_ret, s_msg)

    s_msg = 'Succeed to rolling-update  App {}'.format(name)
    return (b_ret, s_msg)

def kube_deploy_reloadbalance(name, namespace, d_app):
    """Re-loadbalance deployment resource."""
    if not name:
        s_msg = 'name is not defined.'
        return (False, s_msg)
    if not namespace:
        s_msg = 'namespace is not defined.'
        return (False, s_msg)
    if not d_app:
        s_msg = 'app data is not defined.'
        return (False, s_msg)

    # re-loadbalance deploy using
    # k patch svc mydebian -p '{"spec": {"deprecatedPublicIPs": [
    # "192.168.24.42" ], "externalIPs": ["192.168.24.42"]}}'
    s_external_ips = ",".join(['"' + s + '"' for s in d_app['externalIPs']])
    s_patch = '{{"spec":{{"deprecatedPublicIPs":[{0}],"externalIPs":[{0}]}}}}'\
                .format(s_external_ips)
    s_cmd= "{} --kubeconfig {} patch svc/{} -n {} -p '{}'".format( \
            KUBECTL, KUBECONFIG, name, namespace, s_patch)
    log.debug(s_cmd)
    (b_ret, l_out) = cmd(s_cmd)

    if not b_ret:
        log.error(l_out)
        s_msg = 'Fail to re-loadbalance App {}'.format(name)
        return (b_ret, s_msg)

    s_msg = 'Succeed to re-loadbalance  App {}'.format(name)
    return (b_ret, s_msg)

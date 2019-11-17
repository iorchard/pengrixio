import ast
import uuid
import etcd
import json
import requests

import logging
import logging.config

from datetime import datetime

from pengrixio.database import etcdc
from pengrixio.k8s.pod import kube_list_pod
from pengrixio.k8s.namespace import kube_list_namespace
from pengrixio.k8s.namespace import kube_create_namespace
from pengrixio.k8s.namespace import kube_delete_namespace


logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

def get_project(name=None):
    """Get project list.
    """
    l_project = list()

    for item in kube_list_namespace():
        d = dict()
        d['name'] = item.metadata.name
        d['uid'] = item.metadata.uid
        d['status'] = item.status.phase
        d['createdAt'] = item.metadata.creation_timestamp
        # Get number of pod in each host.
        l_pods = kube_list_pod(namespace=d['name'])
        d['pods'] = len(l_pods)
        l_project.append(d)

    return l_project

def create_project(data):
    """Create project
    projectPostSerializer
    """
    if not data.get('name'):
        return (False, 'Project name should be specified.')

    t_ret = (False, '')
    b = kube_create_namespace(data['name'])
    if not b:
        t_ret = (False, '')
    else:
        t_ret = (True, 'project {} is created.'.format(data['name']))

    return t_ret


def delete_project(name):
    """Delete project.
    """
    if not name:  # <name> should be specified.
        return (False, 'Project name should be specified.')
        
    t_ret = (False, '')
    d = kube_delete_namespace(name)
    if not d:
        t_ret = (False, '')
    else:
        t_ret = (True, 'project {} is deleted.'.format(name))

    return t_ret


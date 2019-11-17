import kubernetes.config

import logging
import logging.config

from pengrixio.config import KUBECONFIG

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

# load kubernetes config file.
try:
    kubernetes.config.load_kube_config(KUBECONFIG)
except:
    log.warn('kubernetes cluster config file is invalid.')

import os
import etcd

from etcd import Client
from pengrixio.settings import ETCD_HOST, ETCD_PORT, ETCD_PROTO, ETCD_PREFIX
from pengrixio.settings import ETCD_CERT, ETCD_CA_CERT

# check if ETCD_PROTO is https but there is no ETCD_CERT and ETCD_CA_CERT.
if ETCD_PROTO == 'https':
    for f in ETCD_CERT:
        if not os.path.isfile(f):
            raise Exception('Fail to set ETCD: File not found {}'.format(f))
    if not os.path.isfile(ETCD_CA_CERT):
        raise Exception('Fail to set ETCD: File not found {}'.format(f))

# Read ETCD_CA_CERT if it exists.
if ETCD_PROTO == 'https':
    s_cacert = ''
    with open(ETCD_CA_CERT, 'r') as f:
        s_cacert = f.read()
    etcdc = Client(
            host=ETCD_HOST,
            port=ETCD_PORT,
            allow_reconnect=True,
            protocol=ETCD_PROTO,
            cert=ETCD_CERT,
            ca_cert=ETCD_CA_CERT
    )
else:
    etcdc = Client(
            host=ETCD_HOST,
            port=ETCD_PORT,
            allow_reconnect=True,
            protocol=ETCD_PROTO
    )

etcdc.prefix = ETCD_PREFIX

# check if ETCD_PREFIX exists on etcd server. If not, create it.
try:
    r = etcdc.read(etcdc.prefix)
except etcd.EtcdKeyNotFound as e:
    etcdc.write(etcdc.prefix, None, dir=True)


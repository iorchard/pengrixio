from flask_restplus import fields
from pengrixio.api.restplus import api

edgeSerializer = api.model('Edge', {
    'name': fields.String(required=True, description='edge name'),
    'uid': fields.String(required=True, description='edge uuid'),
    'endpoint': fields.String(required=True, description='edge endpoint'),
    'broker': fields.String(required=True, description='edge broker url'),
    'broker_ip': fields.String(required=True, description='edge broker ip'),
    'hosts': fields.Integer(required=True, description='edge host #'),
    'tenants': fields.Integer(required=True, description='edge tenant #'),
    'apps': fields.Integer(required=True, description='edge app #'),
    'cpu': fields.Integer(required=True, description='edge cpu%'),
    'used_cpu': fields.Integer(required=True, description='edge used cores'),
    'tot_cpu': fields.Integer(required=True, description='edge total cores'),
    'memory': fields.Integer(required=True, description='edge memory%'),
    'used_mem': fields.Integer(required=True, description='used mem in GiB'),
    'tot_mem': fields.Integer(required=True, description='total mem in GiB'),
    'storage': fields.Integer(required=True, description='edge storage in GiB'),
    'used_stor': fields.Integer(required=True, description='edge used storage in GiB'),
    'tot_stor': fields.Integer(required=True, description='edge total storage in GiB'),
    'apps': fields.Integer(required=True, description='edge storage app #'),
    'desc': fields.String(required=True, description='edge base image'),
    'status': fields.String(required=True, description='edge status'),
    'createdAt': fields.DateTime(required=True, description='edge created'),
    'modifiedAt': fields.DateTime(required=True, description='edge modified'),
})
edgePostSerializer = api.model('CreateEdge', {
    'name': fields.String(required=True, description='edge name'),
    'endpoint': fields.String(required=True, description='edge endpoint'),
    'broker': fields.String(required=True, description='edge broker url'),
    'broker_ip': fields.String(required=True, description='edge broker ip'),
    'desc': fields.String(description='edge base image'),
})
edgePatchSerializer = api.model('ModifyEdge', {
    'endpoint': fields.String(required=True, description='edge endpoint'),
    'broker': fields.String(required=True, description='edge broker url'),
    'broker_ip': fields.String(required=True, description='edge broker ip'),
    'desc': fields.String(description='edge base image'),
})

from flask_restplus import fields
from pengrixio.api.restplus import api

app_fields = api.model('App', {
    'name': fields.String(required=True),
    'logo': fields.String(required=True),
    'type': fields.String(required=True),
    'user': fields.String(required=True),
    'status': fields.String(required=False),
    'desc': fields.String(required=False),
})

tenantSerializer = api.model('Tenant', {
    'name': fields.String(required=True, description='tenant name'),
    'uid': fields.String(required=True, description='tenant uuid'),
    'edge': fields.String(required=True, description='tenant endpoint'),
    'app': fields.List(
            fields.Nested(app_fields)
            ),
    'desc': fields.String(required=True, description='tenant base image'),
    'createdAt': fields.DateTime(required=True, description='tenant created'),
})
tenantPostSerializer = api.model('CreateTenant', {
    'name': fields.String(required=True, description='tenant name'),
    'edge': fields.String(required=True, description='edge for tenant'),
    'desc': fields.String(description='tenant description'),
})

from flask_restplus import fields
from pengrixio.api.restplus import api

catalogSerializer = api.model('Catalog', {
    'name': fields.String(required=True, description='catalog name'),
    'type': fields.String(required=False, description='catalog type'),
    'logo': fields.String(required=False, description='catalog logo image'),
    'uid': fields.String(required=False, description='catalog uuid'),
    'cpu_spec': fields.Integer(required=False, description='catalog cpu spec'),
    'mem_spec': fields.Integer(required=False, description='catalog mem spec'),
    'disk_spec': fields.Integer(required=False, description='catalog disk spec'),
    'image_url': fields.String(required=False, description='catalog image url'),
    'desc': fields.String(required=False, description='catalog base image'),
    'createdAt': fields.DateTime(required=False, description='catalog created'),
    'modifiedAt': fields.DateTime(required=False, description='catalog modified'),
})
catalogPostSerializer = api.model('CreateCatalog', {
    'name': fields.String(required=True, description='catalog name'),
    'type': fields.String(required=False, description='catalog type - vm or container'),
    'logo': fields.String(required=False, description='catalog logo image name'),
    'cpu_spec': fields.Integer(required=True, description='catalog cpu spec'),
    'mem_spec': fields.Integer(required=True, description='catalog mem spec'),
    'disk_spec': fields.Integer(required=True, description='catalog disk spec'),
    'image_url': fields.String(required=True, description='catalog image url'),
    'desc': fields.String(description='catalog description'),
})
catalogPatchSerializer = api.model('UpdateCatalog', {
    'type': fields.String(required=False, description='catalog type - vm or container'),
    'logo': fields.String(required=False, description='catalog logo image name'),
    'cpu_spec': fields.Integer(required=True, description='catalog cpu spec'),
    'mem_spec': fields.Integer(required=True, description='catalog mem spec'),
    'disk_spec': fields.Integer(required=True, description='catalog disk spec'),
    'image_url': fields.String(required=True, description='catalog image url'),
    'desc': fields.String(description='catalog description'),
})

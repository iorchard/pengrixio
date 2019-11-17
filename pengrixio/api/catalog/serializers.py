from flask_restplus import fields
from pengrixio.api.restplus import api

catalogSerializer = api.model('Catalog', {
    'name': fields.String(required=True, description='catalog name'),
    'uid': fields.String(required=True, description='catalog uuid'),
    'cpu_spec': fields.Integer(required=True, description='catalog cpu spec'),
    'mem_spec': fields.Integer(required=True, description='catalog mem spec'),
    'disk_spec': fields.Integer(required=True, description='catalog disk spec'),
    'image_url': fields.String(required=True, description='catalog image url'),
    'desc': fields.String(required=True, description='catalog base image'),
    'createdAt': fields.DateTime(required=True, description='catalog created'),
})
catalogPostSerializer = api.model('CreateCatalog', {
    'name': fields.String(required=True, description='catalog name'),
    'cpu_spec': fields.Integer(required=True, description='catalog cpu spec'),
    'mem_spec': fields.Integer(required=True, description='catalog mem spec'),
    'disk_spec': fields.Integer(required=True, description='catalog disk spec'),
    'image_url': fields.String(required=True, description='catalog image url'),
    'desc': fields.String(description='catalog description'),
})

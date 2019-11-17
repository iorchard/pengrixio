from flask_restplus import fields
from pengrixio.api.restplus import api

projectSerializer = api.model('Project', {
    'name': fields.String(required=True, description='project name'),
    'pods': fields.Integer(required=True, description='project pod #'),
    'uid': fields.String(required=True, description='project uuid'),
    'status': fields.String(required=True, description='project status'),
    'createdAt': fields.DateTime(required=True, description='project created'),
})
projectPostSerializer = api.model('CreateProject', {
    'name': fields.String(required=True, description='project name'),
})

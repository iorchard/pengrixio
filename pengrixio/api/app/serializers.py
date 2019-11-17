from flask_restplus import fields
from pengrixio.api.restplus import api

appSerializer = api.model('Apps', {
    'name': fields.String(required=True, description='app name'),
    'uid': fields.String(required=True, description='app uuid'),
    'catalog': fields.String(required=True, description='app from catalog'),
    'user': fields.String(required=True, description='app user'),
    'tenant': fields.String(required=True, description='app on tenant'),
    'state': fields.String(required=True,
        description='building/stopped/running'),
    'desc': fields.String(required=True, description='app base image'),
    'createdAt': fields.DateTime(required=True, description='app created'),
})
appPostSerializer = api.model('CreateApps', {
    'name': fields.String(required=True, description='app name'),
    'catalog': fields.String(required=True, description='app from catalog'),
    'user': fields.String(required=True, description='app user'),
    'desc': fields.String(description='app description'),
})

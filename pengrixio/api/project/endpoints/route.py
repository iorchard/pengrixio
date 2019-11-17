import logging
import logging.config

from flask import request
from flask import abort
from flask import render_template
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from pengrixio.api.restplus import api

from pengrixio.api.project.serializers import projectSerializer
from pengrixio.api.project.serializers import projectPostSerializer

from pengrixio.api.project.bizlogic import get_project
from pengrixio.api.project.bizlogic import create_project
from pengrixio.api.project.bizlogic import delete_project

log = logging.getLogger('pengrixio')

ns = api.namespace('project', description="Operations for project")

@ns.route('/')
class ProjectCollection(Resource):

    @api.marshal_list_with(projectSerializer)
    @jwt_required
    def get(self):
        """Returns list of project."""
        l_project = get_project()
        return l_project

    @api.response(201, 'Project successfully created.')
    @api.expect(projectPostSerializer)
    @jwt_required
    def post(self):
        """Creates a new project.
        """
        data = request.json
        (b_ret, s_msg) = create_project(data)
        if not b_ret:
            d_msg = {'error': 'Project creation is failed.'}
            return d_msg, 400

        # Get a newly created project info.
        #l_project = get_project(data['name'])

        return {}, 201

@ns.route('/<string:name>')
@api.response(404, 'Project not found.')
class ProjectItem(Resource):

    @api.marshal_with(projectSerializer)
    @api.doc('get_something')
    @jwt_required
    def get(self, name):
        """Returns the project information."""
        l_project = get_project(name)
        if not len(l_project):
            d_msg = {'error': 'name {} is not found.'.format(name)}
            return d_msg, 404

        return l_project[0]

    @api.response(204, "The project is successfully deleted.")
    @jwt_required
    def delete(self, name):
        """Deletes the project."""
        (b_ret, s_msg) = delete_project(name)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204

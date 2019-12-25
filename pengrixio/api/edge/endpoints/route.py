import logging
import logging.config

from flask import request
from flask import abort
from flask import render_template
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from pengrixio.api.restplus import api

from pengrixio.api.edge.serializers import edgeSerializer
from pengrixio.api.edge.serializers import edgePostSerializer
from pengrixio.api.edge.serializers import edgePatchSerializer

from pengrixio.api.edge.bizlogic import get_edge
from pengrixio.api.edge.bizlogic import get_edge_info
from pengrixio.api.edge.bizlogic import create_edge
from pengrixio.api.edge.bizlogic import delete_edge
from pengrixio.api.edge.bizlogic import update_edge

log = logging.getLogger('pengrixio')

ns = api.namespace('edge', description="Operations for edge")

@ns.route('/')
class EdgeCollection(Resource):

    @api.marshal_list_with(edgeSerializer)
    @jwt_required
    def get(self):
        """Returns list of edge."""
        l_edge = get_edge()
        return l_edge

    @api.response(201, 'Edge successfully created.')
    @api.expect(edgePostSerializer)
    @jwt_required
    def post(self):
        """Creates a new edge.
        """
        data = request.json
        (b_ret, s_msg) = create_edge(data)
        if not b_ret:
            d_msg = {'error': 'Edge creation is failed.'}
            return d_msg, 400

        # Get a newly created edge info.
        #l_edge = get_edge(data['name'])

        return {}, 201

@ns.route('/<string:name>/')
@api.response(404, 'Edge not found.')
class EdgeItem(Resource):

    @api.marshal_with(edgeSerializer)
    @api.doc('get_something')
    @jwt_required
    def get(self, name):
        """Returns the edge information."""
        (b_ret, d_edge) = get_edge_info(name)
        if not b_ret:
            d_msg = {'error': '{}'.format(d_edge)}
            return d_msg, 404

        return d_edge

    @api.response(204, "The edge is successfully deleted.")
    @jwt_required
    def delete(self, name):
        """Deletes the edge."""
        (b_ret, s_msg) = delete_edge(name)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204

    @api.expect(edgePatchSerializer)
    @api.response(204, "The edge is successfully updated.")
    @jwt_required
    def patch(self, name):
        """Update the edge information."""
        data = request.json
        (b_ret, s_msg) = update_edge(name, data)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204


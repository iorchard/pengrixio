import logging
import logging.config

from flask import request
from flask import abort
from flask import render_template
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from pengrixio.api.restplus import api

from pengrixio.api.catalog.serializers import catalogSerializer
from pengrixio.api.catalog.serializers import catalogPostSerializer
from pengrixio.api.catalog.serializers import catalogPatchSerializer

from pengrixio.api.catalog.bizlogic import get_catalog
from pengrixio.api.catalog.bizlogic import create_catalog
from pengrixio.api.catalog.bizlogic import delete_catalog
from pengrixio.api.catalog.bizlogic import update_catalog

log = logging.getLogger(__name__)

ns = api.namespace('catalog', description="Operations for catalog")

@ns.route('/')
class CatalogCollection(Resource):

    @api.marshal_list_with(catalogSerializer)
    @jwt_required
    def get(self):
        """Returns list of catalog."""
        l_catalog = get_catalog()
        return l_catalog

    @api.response(201, 'Catalog successfully created.')
    @api.expect(catalogPostSerializer)
    @jwt_required
    def post(self):
        """Creates a new catalog.
        """
        data = request.json
        (b_ret, s_msg) = create_catalog(data)
        if not b_ret:
            d_msg = {'error': 'Catalog creation is failed.'}
            return d_msg, 400

        # Get a newly created catalog info.
        #l_catalog = get_catalog(data['name'])

        return {}, 201

@ns.route('/<string:name>/')
@api.response(404, 'Catalog not found.')
class CatalogItem(Resource):

    @api.marshal_with(catalogSerializer)
    @api.doc('get_something')
    @jwt_required
    def get(self, name):
        """Returns the catalog information."""
        l_catalog = get_catalog(name)
        if not len(l_catalog):
            d_msg = {'error': 'name {} is not found.'.format(name)}
            return d_msg, 404

        return l_catalog[0]

    @api.response(204, "The catalog is successfully deleted.")
    @jwt_required
    def delete(self, name):
        """Deletes the catalog."""
        (b_ret, s_msg) = delete_catalog(name)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204

    @api.response(204, "The catalog is successfully updated.")
    @jwt_required
    def patch(self, name):
        """Updates the catalog."""
        data = request.json
        (b_ret, s_msg) = update_catalog(name, data)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404


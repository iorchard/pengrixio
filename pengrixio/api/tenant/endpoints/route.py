import logging
import logging.config

from flask import request
from flask import abort
from flask import render_template
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from pengrixio.api.restplus import api

from pengrixio.api.tenant.serializers import tenantSerializer
from pengrixio.api.tenant.serializers import tenantPostSerializer

from pengrixio.api.tenant.bizlogic import get_tenant
from pengrixio.api.tenant.bizlogic import create_tenant
from pengrixio.api.tenant.bizlogic import delete_tenant

log = logging.getLogger('pengrixio')

ns = api.namespace('tenant', description="Operations for tenant")

@ns.route('/', '/<string:edge_name>/')
class TenantCollection(Resource):

    @api.marshal_list_with(tenantSerializer)
    #@jwt_required
    def get(self, edge_name=None):
        """Returns list of tenant."""
        l_tenant = get_tenant(edge_name)
        return l_tenant

    @api.response(201, 'Tenant successfully created.')
    @api.expect(tenantPostSerializer)
    @jwt_required
    def post(self, edge_name):
        """Creates a new tenant.
        """
        data = request.json
        (b_ret, s_msg) = create_tenant(data)
        if not b_ret:
            d_msg = {'error': 'Tenant creation is failed.'}
            return d_msg, 400

        # Get a newly created tenant info.
        #l_tenant = get_tenant(data['name'])

        return {}, 201

@ns.route('/<string:name>/')
@api.response(404, 'Tenant not found.')
class TenantItem(Resource):

    @api.marshal_with(tenantSerializer)
    @api.doc('get_something')
    @jwt_required
    def get(self, name):
        """Returns the tenant information."""
        l_tenant = get_tenant(name)
        if not len(l_tenant):
            d_msg = {'error': 'name {} is not found.'.format(name)}
            return d_msg, 404

        return l_tenant[0]

    @api.response(204, "The tenant is successfully deleted.")
    @jwt_required
    def delete(self, name):
        """Deletes the tenant."""
        (b_ret, s_msg) = delete_tenant(name)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204

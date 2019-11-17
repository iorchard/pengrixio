import json
import logging
import logging.config

from flask import request
from flask_restplus import Resource

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt_claims

from pengrixio.api.restplus import api
from pengrixio.decorators import authz_required

from pengrixio.config import ADMIN_ID

from pengrixio.api.account.serializers import accountSerializer
from pengrixio.api.account.serializers import accountPostSerializer
from pengrixio.api.account.serializers import accountAuthSerializer
from pengrixio.api.account.serializers import accountPatchSerializer
from pengrixio.api.account.serializers import accountPasswordSerializer
from pengrixio.api.account.serializers import accountUserPasswordSerializer

from pengrixio.api.account.bizlogic import get_account
from pengrixio.api.account.bizlogic import create_account
from pengrixio.api.account.bizlogic import update_account
from pengrixio.api.account.bizlogic import admin_auth_account
from pengrixio.api.account.bizlogic import auth_account
from pengrixio.api.account.bizlogic import delete_account
from pengrixio.api.account.bizlogic import password_account
from pengrixio.api.account.bizlogic import user_password_account

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

ns = api.namespace('account', description="Operations for user accounts")

@ns.route('/')
class AccountCollection(Resource):

    @api.marshal_list_with(accountSerializer)
    @authz_required('admin')
    def get(self):
        """Returns list of account."""
        l_account = get_account()
        return l_account

    @api.response(201, 'Account is successfully created.')
    #@api.expect(accountPostSerializer)
    @authz_required('admin')
    def post(self):
        """Creates a new user account."""
        data = request.json
        log.debug(data)
        (b_ret, s_msg) = create_account(data)
        log.debug((b_ret, s_msg))
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 409
        # get a created account.
        l_account = get_account(data['name'])
        return l_account[0], 201

@ns.route('/admin/login/')
class AdminAccountAuth(Resource):

    @api.response(200, 'Account is successfully authenticated.')
    @api.expect(accountAuthSerializer)
    def post(self):
        """Authenticate an account.
        """
        data = request.json
        if data['name'] != ADMIN_ID:
            d_msg = { 'error': 'Authentication is failed.' }
            return d_msg, 401

        b_ret = admin_auth_account(data)
        if not b_ret:
            d_msg = {'error': 'Admin Authentication is failed.'}
            return d_msg, 401

        # create token
        d_resp = {
            'token': create_access_token(identity=data['name']),
            'refresh_token': create_refresh_token(identity=data['name']),
            'role': 'admin'
        }

        return d_resp, 200

@ns.route('/login')
class AccountAuth(Resource):

    @api.response(200, 'Account is successfully authenticated.')
    @api.expect(accountAuthSerializer)
    def post(self):
        """Authenticate an account.
        """
        data = request.json
        if data['name'] == ADMIN_ID:
            d_msg = { 'error': 'Authentication is failed.' }
            return d_msg, 401

        (b_ret, s_ret) = auth_account(data)
        if not b_ret:
            s_msg = 'Authentication is failed. '
            if s_ret == 'Disabled':
                d_msg = { 'error': s_msg + 'Account is disabled.' }
            elif s_ret == 'Locked':
                d_msg = { 'error': s_msg + 'Account is locked.' }
            elif s_ret == 'Expired':
                d_msg = { 'error': s_msg + 'Account is expired.' }
            else:
                d_msg = { 'error': s_msg }
            return d_msg, 401

        # create token
        d_resp = {
            'token': create_access_token(identity=data['name']),
            'refresh_token': create_refresh_token(identity=data['name']),
            'role': s_ret
        }

        return d_resp, 200

@ns.route('/refresh')
class AccountRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        """Refresh an account token.
        """
        uid = get_jwt_identity()
        log.debug(uid)
        d_resp = {
            'token': create_access_token(identity=uid)
        }
        return d_resp, 200

@ns.route('/<string:name>')
@api.response(404, 'Account not found.')
class AccountItem(Resource):

    @api.marshal_with(accountSerializer)
    @api.doc('get_something')
    @jwt_required
    def get(self, name):
        """Returns the account information."""
        l_account = get_account(name)
        log.debug(len(l_account))
        if not len(l_account):
            log.debug(l_account)
            return {'error': 'name {} not found.'.format(name)}, 404

        return l_account[0]

    @api.expect(accountPatchSerializer)
    @api.response(204, "The account is successfully updated.")
    @jwt_required
    def patch(self, name):
        """Updates the account information."""
        data = request.json
        log.debug(data)
        (b_ret, s_msg) = update_account(name, data)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        l_account = get_account(name)
        return l_account[0], 200

    @api.response(204, "The account is successfully deleted.")
    @authz_required('admin')
    def delete(self, name):
        """Deletes the account."""
        (b_ret, s_msg) = delete_account(name)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204

@ns.route('/<string:name>/pass')
@api.response(404, 'Account not found.')
class AccountPassword(Resource):

    #@ns.expect(accountPasswordSerializer)
    @ns.response(204, "The account is successfully updated.")
    @authz_required('admin')
    def patch(self, name):
        """Updates the account password."""
        data = request.json
        (b_ret, s_msg) = password_account(data)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 400

        l_account = get_account(name)
        return l_account[0], 200

@ns.route('/<string:name>/userpass')
@api.response(404, 'Account not found.')
class AccountUserPassword(Resource):

    @ns.expect(accountUserPasswordSerializer)
    @ns.response(204, "The account is successfully updated.")
    @jwt_required
    def patch(self, name):
        """Updates the account password as user role."""
        d_claim = get_jwt_claims()
        # check authz: only user itself.
        if name != d_claim['id']:
            abort(401, 'Not authorized.')

        data = request.json
        (b_ret, s_msg) = user_password_account(data)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 400

        l_account = get_account(name)
        return l_account[0], 200

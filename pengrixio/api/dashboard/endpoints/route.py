import logging
import logging.config

from flask import request
from flask import abort
from flask import render_template
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from pengrixio.api.restplus import api

from pengrixio.api.dashboard.serializers import dashboardSerializer

from pengrixio.api.dashboard.bizlogic import get_dashboard

log = logging.getLogger('pengrixio')

ns = api.namespace('dashboard', description="Operations for dashboard")

@ns.route('/')
class DashboardCollection(Resource):

    @api.marshal_list_with(dashboardSerializer)
    @jwt_required
    def get(self):
        """Returns list of dashboard."""
        l_dashboard = get_dashboard()
        return l_dashboard

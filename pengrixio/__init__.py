from flask import Flask
from flask import Blueprint
from flask_jwt_extended import JWTManager

from pengrixio import settings
from pengrixio.config import JWT_SECRET_KEY
from pengrixio.config import JWT_ACCESS_TOKEN_EXPIRES

from pengrixio.api.account.endpoints.route import ns as account_ns
from pengrixio.api.project.endpoints.route import ns as project_ns
from pengrixio.api.edge.endpoints.route import ns as edge_ns
from pengrixio.api.tenant.endpoints.route import ns as tenant_ns
from pengrixio.api.catalog.endpoints.route import ns as catalog_ns
from pengrixio.api.app.endpoints.route import ns as app_ns

from pengrixio.api.restplus import api

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)

    with app.app_context():
        blueprint = Blueprint('api', __name__, url_prefix='/api')
        app.register_blueprint(blueprint)
        api = init_api(blueprint)
        api.add_namespace(account_ns)
        api.add_namespace(edge_ns)
        api.add_namespace(tenant_ns)
        api.add_namespace(catalog_ns)
        api.add_namespace(app_ns)

    return app

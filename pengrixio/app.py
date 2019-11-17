import json

from flask import Flask
from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS

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

from pengrixio.config import ADMIN_ID
from pengrixio.api.account.bizlogic import get_account

app = Flask(__name__)
app.secret_key = JWT_SECRET_KEY

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    # get role of identity
    s_role = 'user'
    if identity == ADMIN_ID:
        s_role = 'admin'
    else:
        l_account = get_account(identity)
        if len(l_account) and 'role' in l_account[0]:
            s_role = l_account[0]['role']

    return {
        'id': identity,
        'role': s_role
    }

CORS(app)

def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = \
                                settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    # JWT config
    flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES

    # Be generous on non-trailing-slash url
    flask_app.url_map.strict_slashes = False

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(account_ns)
    api.add_namespace(project_ns)
    api.add_namespace(edge_ns)
    api.add_namespace(tenant_ns)
    api.add_namespace(catalog_ns)
    api.add_namespace(app_ns)

    flask_app.register_blueprint(blueprint)

initialize_app(app)

if __name__ == "__main__":
    app.run(
        debug=settings.FLASK_DEBUG,
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
    )

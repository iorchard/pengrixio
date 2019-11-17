from functools import wraps
from flask_restplus import abort
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_claims

import logging
import logging.config

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

def authz_required(role='admin'):
    def authz_deco(f):
        @wraps(f)
        @jwt_required
        def decorated_function(*args, **kwargs):
            # Get role.
            d_claim = get_jwt_claims()
            log.debug(d_claim)
            if d_claim['role'] != 'admin':
                if 'role' not in d_claim or d_claim['role'] != role:
                    d_msg = {'error': 'Authorization failed.'}
                    log.debug(d_msg)
                    abort(401)
            return f(*args, **kwargs)
        return decorated_function
    return authz_deco

import datetime

from flask_restplus import fields
from pengrixio.api.restplus import api

accountSerializer = api.model('Account', {
    'name': fields.String(required=True, description='user name'),
    'uid': fields.String(required=True, description='user id(uuid)'),
    #'salt': fields.String(required=True, description='bcrypt salt'),
    #'pass': fields.String(required=True, description='bcrypt hash'),
    'role': fields.String(required=True, default='user'),
    'cn': fields.String(required=True, description='user common name'),
    'state': fields.String(required=False, description='user state'),
    'tenant': fields.String(required=False, description='tenant user belongs to'),
    'desc': fields.String(required=False, description='user description'),
    'expireAt': fields.DateTime(required=False, description='pass expire date'),
    'createdAt': fields.DateTime(required=True, description='user created'),
    'modifiedAt': fields.DateTime(required=False, description='user mod time'),
})
accountPostSerializer = api.model('RegisterAccount', {
    'name': fields.String(required=True, description='user name'),
    'pass': fields.String(required=True, description='plaintext password'),
    'cn': fields.String(required=True, description='user common name'),
    'role': fields.String(required=True, default='user'),
    'state': fields.String(
                 required=True,
                 default="Enabled",  # Enabled, Disabled, Locked
             ),
    'desc': fields.String(required=False, description='user description'),
    'tenant': fields.String(required=False, description='tenant user belongs to'),
    'expireAt': fields.DateTime(
                    required=True,
                    default=datetime.datetime.now() +
                                datetime.timedelta(days=90),
                    description='pass expire date'
                ),
})
accountAuthSerializer = api.model('AuthAccount', {
    'name': fields.String(required=True, description='user name'),
    'pass': fields.String(required=True, description='plaintext password'),
})
accountPatchSerializer = api.model('ModifyAccount', {
    'cn': fields.String(required=False, description='account common name'),
    'pass': fields.String(required=False, description='plaintext password'),
    'role': fields.String(required=False),
    'state': fields.String(
                 required=False,
                 default="Enabled",  # Enabled, Disabled, Locked
             ),
    'desc': fields.String(required=False, description='account description'),
    'projects': fields.List(fields.String),
    'expireAt': fields.DateTime(
                    required=True,
                    default=datetime.datetime.now() +
                                datetime.timedelta(days=90),
                    description='pass expire date'
                ),
})
accountPasswordSerializer = api.model('PasswordAccount', {
    'name': fields.String(required=True, description='account name'),
    'pass': fields.String(required=True, description='plaintext password'),
    'pass2': fields.String(required=True, description='plaintext password'),
})
accountUserPasswordSerializer = api.model('UserPasswordAccount', {
    'name': fields.String(required=True, description='account name'),
    'pass': fields.String(required=True, description='plaintext password'),
    'pass1': fields.String(required=True, description='plaintext password'),
    'pass2': fields.String(required=True, description='plaintext password'),
})

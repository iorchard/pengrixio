import ast
import uuid
import etcd
import bcrypt
import logging
import logging.config

from datetime import datetime
from datetime import timedelta

from pengrixio.database import etcdc
from pengrixio.config import ADMIN_ID
from pengrixio.config import ADMIN_SALT
from pengrixio.config import ADMIN_PW

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')

def get_account(name=None):
    """Get account list.
    """
    l_account = list()
    if name is None:  # get all account.
        s_rsc = '{}/account'.format(etcdc.prefix)
    else:
        s_rsc = '{}/account/{}'.format(etcdc.prefix, name)

    try: 
        r = etcdc.read(s_rsc, recursive=True, sorted=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
    else:
        for child in r.children:
            if child.value is not None:
                # need to use ast to convert str to dict.
                d = ast.literal_eval(child.value)
                l_account.append(d)
    finally:
        return l_account

def create_account(data):
    """Create account.
    etcd_key: <ETCD_PREFIX>/account/<name>
    """
    t_ret = (False, '')
    s_rsc = ''
    # Create uid(uuid) for account
    s_uuid = str(uuid.uuid4())
    # Get iso 8601 format datetime for created timestamp
    s_created = datetime.utcnow().isoformat() + 'Z'
    # Put s_created into data dict.
    data['createdAt'] = s_created
    data['uid'] = s_uuid
    bytes_salt = bcrypt.gensalt()
    data['pass'] = bcrypt.hashpw(str.encode(data['pass']),
                                            bytes_salt).decode()
    data['salt'] = bytes_salt.decode()
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    log.debug(data)
    try:
        etcdc.write(s_rsc, data, prevExist=False)
    except etcd.EtcdKeyAlreadyExist as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'user {} is created.'.format(data['name']))
    finally:
        return t_ret

def admin_auth_account(data):
    """Authenticate admin account.
    data = {'name':, 'pass':}
    """
    b_ret = False
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.debug(e)
        # auth against config file.
        s_pass = bcrypt.hashpw(data['pass'].encode(), 
                               ADMIN_SALT.encode()).decode()
        log.debug(data['name'] + ':' + s_pass)
        if data['name'] == ADMIN_ID and s_pass == ADMIN_PW:
            # Add admin entry in etcd and return True.
            d = dict()
            d['name'] = ADMIN_ID
            d['pass'] = data['pass']
            d['cn'] = 'Admin'
            d['role'] = 'admin'
            d['state'] = 'Enabled'
            s_expire = (datetime.now() + timedelta(days=90)).isoformat() + 'Z'
            d['expireAt'] = s_expire
            (b_ret, s_msg) = create_account(d)
            return b_ret
        else:
            return False
    else:
        d = ast.literal_eval(r.value)
        s_pass = bcrypt.hashpw(data['pass'].encode(), 
                               d['salt'].encode()).decode()
        return data['name'] == ADMIN_ID and s_pass == d['pass']

def auth_account(data):
    """Auth account.
    data = {'name':, 'pass'}
    """
    b_ret = False

    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return b_ret

    d = ast.literal_eval(r.value)
    # check state.
    if d.get('state') and d.get('state') == 'Disabled':
        return (False, 'Disabled')
    elif d.get('state') and d.get('state') == 'Locked':
        return (False, 'Locked')
    elif 'state' not in d or d.get('state') != 'Enabled':
        return (False, 'UnknownError')
    # check expireAt
    if datetime.utcnow().isoformat() > d.get('expireAt'):
        return (False, 'Expired')

    s_pass = bcrypt.hashpw(data['pass'].encode(), 
                           d['salt'].encode()).decode()

    if s_pass != d['pass']:
        return (False, 'PasswordMismatch')

    s_role = d['role'] if 'role' in d else 'user'

    return (True, s_role)


def update_account(name, data):
    """Update account.
    """
    data = dict((k, v) for k, v in data.items() if v)
    t_ret = (False, '')
    if not name:  # <name> should be specified.
        return t_ret
        
    s_rsc = '{}/account/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
        return t_ret

    d = ast.literal_eval(r.value)

    # Get iso 8601 format datetime for modified timestamp
    s_modified = datetime.utcnow().isoformat() + 'Z'
    # Put s_modified into data dict.
    data['modifiedAt'] = s_modified
    d.update(data.items())
    try:
        etcdc.write(s_rsc, d, prevExist=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'user {} is updated.'.format(name))
    finally:
        return t_ret

def delete_account(name):
    """Delete account.
    """
    t_ret = (False, '')
    if not name:  # <name> should be specified.
        return t_ret
        
    s_rsc = '{}/account/{}'.format(etcdc.prefix, name)
    try:
        r = etcdc.delete(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'user {} is deleted.'.format(name))
    finally:
        return t_ret

def password_account(data):
    """Modify account password.
    etcd_key: <ETCD_PREFIX>/account/<name>
    data: {'name': , 'pass': , 'pass2': }
    """
    t_ret = (False, '')
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return (False, 'EtcdKeyNotFound')

    d = ast.literal_eval(r.value)

    # check data['pass'] is valid.
    (b_ret, s_msg) = _pass_validate(data)
    if not b_ret:
        log.debug((b_ret, s_msg))
        return (b_ret, s_msg)

    # password is okay. go head.
    new_data = dict()
    s_modified = datetime.utcnow().isoformat() + 'Z'
    data['modifiedAt'] = s_modified
    # Put d['pass'] to oldpass entry.
    if 'oldpass' in d:
        new_data['oldpass'].append(d['pass'])
    else:
        new_data['oldpass'] = [d['pass']]

    # Create new hashed password.
    bytes_salt = bytes(d['salt'], 'utf-8')
    new_data['pass'] = bcrypt.hashpw(str.encode(data['pass']),
                                            bytes_salt).decode()
    d.update(new_data.items())
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        etcdc.write(s_rsc, d, prevExist=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'user {} password is modified.'.format(data['name']))
    finally:
        return t_ret

def _pass_validate(data):
    """password validation
    * check if pass is not in old pass entry.
    """
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return (False, 'EtcdKeyNotFound')

    d = ast.literal_eval(r.value)

    s_pass = bcrypt.hashpw(data['pass'].encode(), 
                           d['salt'].encode()).decode()
    if s_pass == d['pass']:
        return (False, 'NewPasswordSameAsCurrentPassword')

    if 'oldpass' in d:
        for s_oldpass in d['oldpass']:
            if s_oldpass == s_pass:
                return (False, 'PasswordPreviouslyUsed')

    return (True, 'PasswordMatched')

def user_password_account(data):
    """Modify user account password.
    etcd_key: <ETCD_PREFIX>/account/<name>
    data: {'name': , 'pass': , 'pass1': , 'pass2': }
    """
    t_ret = (False, '')
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        r = etcdc.read(s_rsc)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        return (False, 'EtcdKeyNotFound')

    d = ast.literal_eval(r.value)

    # check if data['pass'] == d['pass']
    s_pass = bcrypt.hashpw(data['pass'].encode(), 
                           d['salt'].encode()).decode()
    if s_pass != d['pass']:  # current password mismatch
        return (False, 'Current password is not matched.')

    # since data['pass'] is matched, overwrite data['pass1'] to data['pass'] 
    # to validate new password.
    data['pass'] = data['pass1']
    (b_ret, s_msg) = _pass_validate(data)
    if not b_ret:
        log.debug((b_ret, s_msg))
        return (b_ret, s_msg)

    # password is okay. go head.
    new_data = dict()
    s_modified = datetime.utcnow().isoformat() + 'Z'
    data['modifiedAt'] = s_modified
    # Put d['pass'] to oldpass entry.
    if 'oldpass' in d:
        d['oldpass'].append(d['pass'])
    else:
        d['oldpass'] = [d['pass']]

    # Create new hashed password.
    bytes_salt = bytes(d['salt'], 'utf-8')
    d['pass'] = bcrypt.hashpw(str.encode(data['pass']),
                                         bytes_salt).decode()
    s_rsc = '{}/account/{}'.format(etcdc.prefix, data['name'])
    try:
        etcdc.write(s_rsc, d, prevExist=True)
    except etcd.EtcdKeyNotFound as e:
        log.error(e)
        t_ret = (False, e)
    else:
        t_ret = (True, 'user {} password is modified.'.format(data['name']))
    finally:
        return t_ret

import bcrypt
import getpass

p = getpass.getpass()

salt = bcrypt.gensalt()
pw = bcrypt.hashpw(bytes(p, 'utf-8'), salt)

print("salt: {}".format(salt))
print("adminpw: {}".format(pw))

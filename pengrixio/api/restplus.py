from flask_restplus import Api

api = Api(version='1.0', 
          title='KT Edge Platform(KEP) API',
          description='KT Edge Computing API',
          contact='jijisa@iorchard.net',
          license='Apache 2.0',
          license_url='http://wherever_license_is_on/',
          endpoint='api',
          validate=True,
      )

def init_api(app):
    api.app = app
    return api

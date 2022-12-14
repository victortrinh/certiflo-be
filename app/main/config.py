import os

basedir = os.path.abspath(os.path.dirname(__file__))

stream = os.popen('heroku config:get DATABASE_URL -a certiflo-be')
output = stream.read()

class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'ghghuvtusdalshurhtycakydiriybae'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://sfewlrtifivowy:3a328968685b4fe6d2a8ca7c146f4292eeaf21779d8c42bd9c032705d4cc49f0@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d2hai88lr5m2tl'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DISABLE_AUTHENTICATION = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or output
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or output
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

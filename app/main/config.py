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
    SQLALCHEMY_DATABASE_URI = 'postgres://lmqqsspkekuaar:d5de1f29813bdb355d79b824b5ad78c2af8be4c487317ca24885060824a0cfb2@ec2-54-208-158-56.compute-1.amazonaws.com:5432/d7448hsfkq2i2q'
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

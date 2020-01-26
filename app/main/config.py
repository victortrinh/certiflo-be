import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'ghghuvtusdalshurhtycakydiriybae'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost:5432/certiflo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://tvyrdwzbnsjfdf:7ab783423f119fcdedd9534ec9f59a07afea1f02fe630c90f10' \
                              '06c88040432f1@ec2-107-20-168-237.compute-1.amazonaws.com:5432/d5c7g5fvfrekii'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://tvyrdwzbnsjfdf:7ab783423f119fcdedd9534ec9f59a07afea1f02fe630c90f10' \
                              '06c88040432f1@ec2-107-20-168-237.compute-1.amazonaws.com:5432/d5c7g5fvfrekii'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

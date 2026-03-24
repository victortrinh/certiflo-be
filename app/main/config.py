import os


def fix_database_url(url):
    """Heroku uses postgres:// but SQLAlchemy 2.x requires postgresql://."""
    if url and url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql://', 1)
    return url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-fallback-key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_size': 3,
        'pool_recycle': 280,
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = fix_database_url(os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/certiflo'
    ))
    DISABLE_AUTHENTICATION = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = fix_database_url(os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/certiflo'
    ))
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = fix_database_url(os.environ.get('DATABASE_URL'))


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

import os
from flask_migrate import Migrate
from app import blueprint
from app.main import create_app, db

config_name = os.environ.get('FLASK_CONFIG', 'dev')
app = create_app(config_name)
app.register_blueprint(blueprint)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()

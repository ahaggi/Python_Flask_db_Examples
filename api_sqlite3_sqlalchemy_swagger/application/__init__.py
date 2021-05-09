from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import connexion

from flask_cors import CORS

# Globally accessible sqlalc and ma
# Note the presence of (sqlalc and ma) and its location: this our database object being set as a global variable outside of create_app(). Inside of create_app(), on the other hand, contains the line sqlalc.init_app(app). Even though we've set our sqlalc object globally, this means nothing until we initialize it after creating our application. We accomplish this by calling init_app() within create_app(), 
sqlalc = SQLAlchemy()
ma = Marshmallow()


def create_app():
    """Initialize the core application."""
    # Create the connexion application instance


    connex_app = connexion.FlaskApp(__name__, specification_dir='./')
    # Read the swagger.yml file to configure the endpoints
    connex_app.add_api('swagger.yml')

    # Get the underlying Flask app instance
    # app = connex_app.app    # app = Flask(__name__, instance_relative_config=False)
    app = connex_app.app
    app.config.from_object('config.Config')


    # Initialize Plugins,, Bind sqlalc to Flask  instead of "sqlalc = SQLAlchemy(app)"
    # After the app object is created, we then "initialize" those plugins we mentioned earlier. Initializing a plugin registers a plugin with our Flask app.
    # Setting sqlalc as global variables outside of init_app() makes it globally accessible to other parts of our application
    sqlalc.init_app(app)
    ma.init_app(app)

    CORS(app)

    with app.app_context():
        # Include our Routes
        # from . import routes

        # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app
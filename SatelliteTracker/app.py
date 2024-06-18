from flask import Flask, redirect, render_template, g, session
from flask_debugtoolbar import DebugToolbarExtension
import logging, os

from app.models import db, connect_db, User
from config import Config, ConfigDev, CURR_USER_KEY
from app.routes import auth_blueprint, user_details_blueprint, homepage_blueprint


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
   
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(homepage_blueprint)
    app.register_blueprint(user_details_blueprint)

    # toolbar = DebugToolbarExtension(app)
    logging.basicConfig(filename='app.log', level=logging.INFO)
    

    @app.before_request
    def add_user_to_g():
        """If we're logged in, add curr user to Flask global."""
        user = None
        if CURR_USER_KEY in session:
            try:
                user = User.query.get(session[CURR_USER_KEY])
            except Exception as e:
                session.pop(CURR_USER_KEY, None)
        g.user = user


    ##############################################################################
    #     error handlers                                                         #
    ##############################################################################

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('/errors/404.html'), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('/errors/500.html'), 500


    @app.errorhandler(403)
    def forbidden(error):
        return render_template('/errors/403.html'), 403


    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('/errors/401.html'), 401

    return app

if __name__ == '__main__':
    print("we are in the __main__ if statement in app.py")
    debug = False
    if os.environ.get('ENVIRONMENT') == 'DEV':
        app = create_app(ConfigDev)
        debug = True

    else:
        app = create_app(Config)
        debug = False

    connect_db(app)
    app.run(port=8080, debug=debug)

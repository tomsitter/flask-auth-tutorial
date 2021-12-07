import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

#init db globally so we can import it into other files
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY") or 'a-secret-key',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'flask-auth.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True,
    )

    # connect db to our app
    db.init_app(app)

    from app.auth.views import auth
    from app.main.views import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    from app.main.errors import page_not_found
    app.register_error_handler(404, page_not_found)

    return app
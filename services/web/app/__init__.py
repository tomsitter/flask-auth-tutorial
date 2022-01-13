import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

# init db globally so we can import it into other files
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY") or 'a-secret-key',
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", 'sqlite://' + os.path.join(basedir, 'flask-auth.sqlite')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True,
        STATIC_FOLDER=f"{os.getenv('APP_FOLDER')}/static",
        MAIL_SERVER='smtp@gmail.com',
        MAIL_USE_TLS=True,
        MAIL_PORT=587,
    )

    # connect db to our app
    db.init_app(app)

    from app.auth.views import auth
    from app.main.views import main
    from app.account.views import account
    from app.gig.views import gig
    from app.admin.views import admin
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(account, url_prefix="/user")
    app.register_blueprint(gig, url_prefix="/gig")
    app.register_blueprint(admin, url_prefix="/admin")

    from app.main.errors import page_not_found
    app.register_error_handler(404, page_not_found)

    return app

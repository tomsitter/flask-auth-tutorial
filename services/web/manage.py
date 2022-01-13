from app import create_app, db
from app.models import User
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from flask import send_from_directory
from flask_mail import Mail

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)
mail = Mail(app)

# makes the db and the User automatically imported in flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()

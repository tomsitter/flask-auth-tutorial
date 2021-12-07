from app import create_app, db
from app.models import User
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


# makes the db and the User automatically imported in flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
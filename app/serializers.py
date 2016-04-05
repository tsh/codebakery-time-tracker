from app import db, create_app
from flask_marshmallow import Marshmallow


app = create_app()
ma = Marshmallow(app)



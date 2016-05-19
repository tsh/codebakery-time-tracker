from app import create_app, db
from app.api import api_v1
from config import DevelopmentConfig

dev_config = DevelopmentConfig()
app = create_app(dev_config)
with app.app_context():
    db.create_all()

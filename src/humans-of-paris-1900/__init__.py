from flask import Flask

from db_models import db
from endpoints import mod

app = Flask(__name__)
app.config.from_object('config.DevConfig')
app.register_blueprint(mod)

db.init_app(app)
bootstrap = True
if bootstrap:
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run()
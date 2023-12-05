from flask import Flask

from myapp.models.task import db
from myapp.schemas.task_schema import ma
from myapp.routes.tasks import tasks_bp
from myapp.config import Config



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)

app.register_blueprint(tasks_bp, url_prefix='/tasks')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

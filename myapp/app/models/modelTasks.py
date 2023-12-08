from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description



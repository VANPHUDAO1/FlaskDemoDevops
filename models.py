from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    logs = db.Column(db.Text, nullable=True)
    monitor_link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<App {self.name}>"

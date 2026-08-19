from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/tasks")
def get_tasks():
    tasks = Task.query.all()
    return {"tasks": [task.to_dict() for task in tasks]}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash   

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SECRET_KEY"] = "dev-secret-key-12345"       

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


class User(db.Model):                                   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/tasks")
def get_tasks():
    tasks = Task.query.all()
    return {"tasks": [task.to_dict() for task in tasks]}


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return task.to_dict(), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.done = data.get("done", task.done)
    db.session.commit()
    return task.to_dict()


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204


@app.route("/register", methods=["POST"])               
def register():
    data = request.get_json()
    hashed = generate_password_hash(data["password"])
    user = User(username=data["username"], password=hashed)
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered"}, 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
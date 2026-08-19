from flask import Flask

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build DevSecOps pipeline", "done": False},
]


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/tasks")
def get_tasks():
    return {"tasks": tasks}


if __name__ == "__main__":
    app.run(debug=True)
from flask import request, jsonify
from app import app, db
from app.models.modelTasks import Task
from app.schemas.schemasTasks import TaskSchema


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


### RUTAS ###
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    new_task = Task(title=title, description=description)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenido a mi API'})


if __name__ == "__main__":
    app.run(debug=True)

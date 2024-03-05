import datetime
from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create flask app
app = Flask(__name__)
# Configure the app based on env variables
app.config.from_object('project.config.Config')

# Init SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import database models
from project.models.task import Task

# Simple hello world route
@app.route('/')
def hello_world():
    return jsonify(hello='world')

# Route to list tasks
@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify(result=tasks)

# Route to create new tasks
# Expects a json body with the 'text' attribute
@app.route('/task', methods=['POST'])
def new_task():
        new_task_json = request.get_json()
        if 'text' in new_task_json:
            new_task = Task(text=new_task_json['text'])
            db.session.add(new_task)
            db.session.commit()
            # Returns the newly added task
            return jsonify(result=new_task), 201
        else:
            return jsonify(error="Missing JSON request body with 'text' attribute."), 400

# Route to update and delete tasks
# The task id is passed in as a route parameter
# If called with the PUT method we check for 'status' or 'text' in the json body and update the task accordingly
# If called with the DELETE method we just delete the task
# In both cases, if the task doesn't exist we throw a 404 not found error
@app.route('/task/<id>', methods=['PUT', 'DELETE'])
def update_or_delete_task(id):
    preexisting_task = db.session.get(Task, id)
    # Check whether the task exists
    if preexisting_task:
        if request.method == 'PUT':
            update_task_json = request.get_json()
            if 'status' in update_task_json:
                preexisting_task.status = update_task_json['status']
            if 'text' in update_task_json:
                preexisting_task.text = update_task_json['text']
            # Update the updated_at time
            preexisting_task.updated_at = datetime.datetime.now(datetime.UTC)
            db.session.commit()
            return jsonify(result=preexisting_task)
        else:
            if preexisting_task:
                db.session.delete(preexisting_task)
                db.session.commit()
                return jsonify(success=True)
    # If the task doesn't exist, return a 404 not found error
    else:
        return jsonify(error='Selected task not found'), 404
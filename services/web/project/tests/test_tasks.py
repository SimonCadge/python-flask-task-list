import datetime
import uuid

from project import db
from project.models.task import Task

def test_hello_world(client):
    response = client.get('/')
    response = response.json
    assert 'hello' in response and response['hello'] == 'world'

def test_list_tasks(client):
    # Manually adding a new task so we can check the /tasks endpoint reads from the db.
    unique = str(uuid.uuid1())
    new_task = Task(text=unique)
    db.session.add(new_task)
    db.session.commit()

    # Get the list of tasks and check whether it includes the one we just added.
    response = client.get('/tasks')
    assert response.status_code == 200
    tasks = response.json['result']
    assert any(map(lambda x: x['text'] == unique, tasks))

def test_new_task_success(client):
    # Create a new task with a unique text field.
    unique = str(uuid.uuid1())
    response = client.post('/task', json={'text': unique})
    # The response should be status 201 and should contain the new task data.
    assert response.status_code == 201
    new_task = response.json['result']
    assert new_task['text'] == unique

    # Get the full list of tasks again and check that the newly added one is there.
    response = client.get('/tasks')
    assert response.status_code == 200
    all_tasks = response.json['result']
    assert new_task in all_tasks

def test_new_task_fail(client):
    # Attempt to add a new task without including the 'text' attribute in the json body.
    response = client.post('/task', json={'other': 'test'})
    # Error status and message explain the error.
    assert response.status_code == 400
    assert response.json['error'] == "Missing JSON request body with 'text' attribute."

    # Attempt to add a new task with no json body.
    response = client.post('/task')
    assert response.status_code == 415

def test_update_task_success(client):
    # Create a new task with a unique text field.
    unique_1 = str(uuid.uuid1())
    response = client.post('/task', json={'text': unique_1})
    assert response.status_code == 201
    new_task = response.json['result']
    assert new_task['status'] == False

    # Note down time pre-update so we can check that updated_at is updated correctly.
    pre_put = datetime.datetime.now(datetime.UTC)

    # Modify the newly added task with new text and status.
    unique_2 = str(uuid.uuid1())
    response = client.put(f"/task/{new_task['id']}", json={'text': unique_2, 'status': True})
    assert response.status_code == 200
    updated_task = response.json['result']
    assert updated_task['text'] == unique_2
    assert updated_task['status'] == True

    # Fetch the task from the db and check that the updated_at datetime was updated.
    updated_task = db.session.get(Task, new_task['id'])
    updated_at = updated_task.updated_at.replace(tzinfo=datetime.timezone.utc)
    assert pre_put < updated_at

    # Fetch all tasks and check that the updated text appears.
    response = client.get('/tasks')
    assert response.status_code == 200
    all_tasks = response.json['result']
    assert any(map(lambda x: x['text'] == unique_2, all_tasks))

def test_update_task_fail(client):
    # Attempt to update a non-existent task.
    response = client.put('/task/1000', json={'text': 'test'})
    # Error code and response explain the error.
    assert response.status_code == 404
    assert response.json['error'] == 'Selected task not found'

    # Attempt to update a task without a request body.
    response = client.put('/task/1')
    assert response.status_code == 415

def test_delete_task_success(client):
    # Create a new task with a unique text field.
    unique = str(uuid.uuid1())
    response = client.post('/task', json={'text': unique})
    assert response.status_code == 201
    inserted_task = response.json['result']

    # Delete that task.
    response = client.delete(f"/task/{inserted_task['id']}")
    assert response.status_code == 200
    assert response.json['success'] == True

    # List all tasks and assert that the deleted task no longer exists.
    response = client.get('/tasks')
    assert response.status_code == 200
    all_tasks = response.json['result']
    assert all(map(lambda x: x['text'] != unique, all_tasks))

def test_delete_task_fail(client):
    # Attempt to delete a non-existent task.
    response = client.delete('/task/1000')
    # Error code and response explain the error.
    assert response.status_code == 404
    assert response.json['error'] == 'Selected task not found'
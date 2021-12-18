from flask import Flask, render_template, request, Response
from flask.json import jsonify

import pickle
import uuid

app = Flask(__name__)


# project id generator
def idGenerator():
  return uuid.uuid4().hex[:24]


def read_pickle_data(inputFileName):
  with open(inputFileName, 'rb') as pickleFile:
    # projekts beolvasása a pickle fileból
    pickleData = pickle.load(pickleFile)
  # a dict többszörösen létrehozta a projects-et azért mélyebb szintől indítottam
  return pickleData[0]


def save_data(dataDict):
  with open('projects.pickle', 'wb') as pickleFile:
    # Vissza konvertálás list-be kiíráshoz
    tmp = []
    tmp.append(dataDict)
    pickle.dump(tmp, pickleFile)


projects = read_pickle_data('projects.pickle')

# projects = [{
#     'name': 'my project',
#     'tasks': [{
#         'name': 'my task',
#         'completed': False
#     }]
# }]


@app.route('/')
def home():
  name = "Niki"
  return render_template('index.html', user_name=name)


@app.route('/project')
def get_projects():
  return jsonify({'projects': projects})


@app.route('/project/<string:project_id>')
def get_project(project_id):
  for project in projects:
    if project['project_id'] == project_id:
      return jsonify(project)
  return jsonify({'message': 'project not found'})


@app.route('/project/<string:name>/task')
def get_all_tasks_in_project(name):
  for project in projects:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
  return jsonify({'message': 'project not found'})


@app.route('/project/<string:project_id>/task', methods=['POST'])
def add_task_to_project(project_id):
  request_data = request.get_json()
  for project in projects:
    if project['project_id'] == project_id:
      new_task = {
          'name': request_data['name'],
          'completed': request_data['completed'],
          'checklist': request_data['checklist']
      }
      # a generált task id hozzáadása
      new_task_id = idGenerator()
      new_task['task_id'] = new_task_id
      project['tasks'].append(new_task)
      save_data(projects)
      # return jsonify(new_task)
      return jsonify({'message': f'task created with id: {new_task_id}'})
  return jsonify({'message': 'project not found'})


@app.route('/project', methods=['POST'])
def create_project():
  # lekérdezzük a http request body-ból a JSON adatot:
  request_data = request.get_json()
  # létrehozom az új projektet
  new_project = {
      'name': request_data['name'],
      'creation_date': request_data['creation_date'],
      'completed': request_data['completed'],
      'tasks': request_data['tasks']
  }
  # a generált projekt id hozzáadása
  new_project_id = idGenerator()
  new_project['project_id'] = new_project_id
  # a létrehozott új projektet belerakom a projektek közé
  projects.append(new_project)
  save_data(projects)
  # return jsonify(new_project)
  return jsonify({'message': f'project created with id: {new_project_id}'})


@app.route('/project/<string:project_id>/complete', methods=['POST'])
def change_project_status(project_id):
  for project in projects:
    if project['project_id'] == project_id:
      if project['completed'] == False:
        project['completed'] = True
        return jsonify(project)
  # Üres string & 200as response code - Link: https://flask.palletsprojects.com/en/2.0.x/api/
  return Response('', status=200)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)

import json
from marathon import MarathonClient
from marathon.models import MarathonApp
from marathon.models import MarathonTask
from marathon.models.container import MarathonContainer
from marathon.models.container import MarathonDockerContainer


def main():

    c = MarathonClient('http://localhost:8080')
    stop_service_instance(c)


def start_service_instance(client):

    """ Starts an app if no one exists, otherwise adds a task
    """

    # Get the number of apps named sleepy running

    app_list = client.list_apps(app_id = 'sleepy')
    
    if len(app_list) == 0:
        app = create_app(client)
        return 'App started :'+app.to_json()
    else:
        deployment = client.scale_app('sleepy', delta = 1) 
        return 'Instance started: '+json.dumps(deployment)
    

def stop_service_instance(client):

    deployment = client.scale_app('sleepy', delta = -1)
    return 'Instance stopped: '+json.dumps(deployment)


def create_app(client):

    app = client.create_app(
        'sleepy', 
        MarathonApp(
            cmd = 'while true; do sleep 33 ; done', 
            mem = 32, 
            cpus = 0.1, 
            container = MarathonContainer(
                docker = MarathonDockerContainer(image='python:3'), 
                type = 'DOCKER'
            )
        )
    )
    return app


def list_service_instances(client):

    task_list = client.list_tasks('sleepy')
    instances = [ MarathonTask.to_json(x) for x in task_list ]
    return ','.join(instances)


def get_service_instance(client, instance_id = 'null'):

    task_list = client.list_tasks('sleepy')
    for task in task_list:
        if task.id == instance_id:
           return task.to_json()


if __name__ == "__main__":
    # execute only if run as a script
    main()

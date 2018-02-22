from marathon import MarathonClient
from marathon.models import MarathonApp
from marathon.models.container import MarathonContainer
from marathon.models.container import MarathonDockerContainer

if __name__ == "__main__":
    # execute only if run as a script
    main()

def main():

    c = MarathonClient('http://localhost:8080')
    start_service_instance(c)
    list_service_instances(c)


def start_service_instance(client):

    """ Starts an app if no one exists, otherwise adds a task
    """

    # Get the number of apps named sleepy running

    app_list = client.list_apps(app_id = 'sleepy')
    
    if len(app_list) == 0:
        create_app(client)
    else:
        client.scale_app('sleepy', delta = 1) 
    

def stop_service_instance(client):

    client.scale_app('sleepy', delta = -1)


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
    return task_list


def get_service_instance(client, instance_id = 'null'):

    task_list = list_service_instances(client)
    for task in task_list:
        if task.id == instance_id:
            instance = task
            return instance


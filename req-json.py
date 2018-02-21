import json
import requests

app_definition = """{
    "id": "spleepy",
    "cmd": "while true; do sleep 33 ; done",
    "cpus": 0.1,
    "mem": 32.0,
    "disk": 0.0,
    "maxLaunchDelaySeconds": 600,
    "instances": 1,
    "container": {
      "type": "DOCKER",
      "docker": {
        "image": "python:3"
      }
    }
}"""

json_app = json.loads(app_definition)
r = requests.post('http://127.0.0.1:8080/v2/apps', json=json_app)
print r

import requests
import json


if __name__ == '__main__':
    """POST test. First, run the server."""
    with open('example_payloads/payload1.json','r') as jsonfile:
        data_json = json.loads(jsonfile.read())
    r = requests.post('http://127.0.0.1:8888/calculate',json=data_json)
    print(r.text)

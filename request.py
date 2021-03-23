from flask import Flask, request,jsonify,render_template
import requests
app = Flask(__name__)
user_data = {
    "username":"admin",
    "password":"SDhxys123!@#"
}
bot_data = {
    "fileId":58,
    "runAsUserIds":[14],
    "botInput": {
        "sDocHello": {
        "type": "STRING",
        "string": "Hello world, go be great."
        }
    }
}

@app.route('/')
def index():
    return 'hello flask'


@app.route("/test",methods=['POST'])
def gettoken():
    r = requests.post("http://82.156.102.131/v1/authentication",json=user_data)
    token = r.json()['token']
    headers = {'X-Authorization': token}
    r1 = requests.post("http://82.156.102.131/v3/automations/deploy",json=bot_data,headers=headers)
    return jsonify({'Code': 'OK'})

@app.route("/getStatus",methods=['POST'])
def getStatus():
    r = requests.post("http://82.156.102.131/v1/authentication", json=user_data)
    token = r.json()['token']
    headers = {'X-Authorization': token}
    file_data = {
          "filter": {
            "operator": "and",
            "operands": [
              {
          "operator": "eq",
          "value": "9",
          "field": "deviceId"
          },
          {
          "operator": "eq",
          "value": "58",
          "field": "fileId"
          }
        ]
        }
    }
    r1 = requests.post("http://82.156.102.131/v2/activity/list", json=file_data, headers=headers)
    return r1.json()



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9900')
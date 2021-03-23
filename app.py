from flask import Flask, request,jsonify,render_template
import requests
import pymssql
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/*')
user_data = {
    "username":"admin",
    "password":"SDhxys123!@#"
}
host = "127.0.0.1:1433"
user = "172_21_0_12\Administrator"
password = "SDhxys123!@#"

@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html', title='login')

@app.route('/home')
def home():
    return render_template('home.html', title='home')

@app.route("/test",methods=['POST'])
def deployBot():
    print(request.get_data(as_text=True))
    rdata = json.loads(request.get_data(as_text=True))
    print(rdata)
    fileId = rdata['fileId']
    userId = rdata['userId']
    bot_data = {
        "fileId": fileId,
        "runAsUserIds": [userId],
        "botInput": {
            "sDocHello": {
                "type": "STRING",
                "string": "Hello world, go be great."
            }
        }
    }
    r = requests.post("http://82.156.102.131/v1/authentication",json=user_data)
    token = r.json()['token']
    headers = {'X-Authorization': token}
    r1 = requests.post("http://82.156.102.131/v3/automations/deploy",json=bot_data,headers=headers)
    return jsonify({'Code': 'OK'})

@app.route("/getStatus",methods=['POST'])
def getStatus():
    rdata = json.loads(request.get_data(as_text=True))
    deviceId = rdata['deviceId']
    fileId = rdata['fileId']
    r = requests.post("http://82.156.102.131/v1/authentication", json=user_data)
    token = r.json()['token']
    headers = {'X-Authorization': token}
    file_data = {
          "filter": {
            "operator": "and",
            "operands": [
              {
          "operator": "eq",
          "value": deviceId,
          "field": "deviceId"
          },
          {
          "operator": "eq",
          "value": fileId,
          "field": "fileId"
          }
        ]
        }
    }
    r1 = requests.post("http://82.156.102.131/v2/activity/list", json=file_data, headers=headers)
    return r1.json()

@app.route("/getDevice",methods=['POST'])
def getDevice():
    conn = pymssql.connect(host=host, user=user, password=password, database="AA", charset="utf8")
    cur = conn.cursor()
    cur.execute("select deviceName,deviceId,userId from device")
    data = cur.fetchall()
    for i in range(0,len(data)):
        data[i] = {
            'deviceName':data[i][0],
            'deviceId':data[i][1],
            'userId': data[i][2],
        }
    return jsonify(data)

@app.route("/getFile",methods=['POST'])
def getFile():
    r = requests.post("http://82.156.102.131/v1/authentication", json=user_data)
    token = r.json()['token']
    headers = {'X-Authorization': token}
    conn = pymssql.connect(host=host, user=user, password=password, database="AA", charset="utf8")
    cur = conn.cursor()
    cur.execute("select fileName,fileId from filelist")
    data = cur.fetchall()
    for i in range(0,len(data)):
        file_data = {
            "filter": {
                "operator": "and",
                "operands": [
                    {
                        "operator": "eq",
                        "value": data[i][1],
                        "field": "fileId"
                    }
                ]
            }
        }
        r1 = requests.post("http://82.156.102.131/v2/activity/list", json=file_data, headers=headers)
        data[i] = {
            'fileName':data[i][0],
            'fileId':data[i][1],
            'status':(r1.json()['list'][len(r1.json()['list'])-1]['status'])
        }
    cur.execute("select deviceName,deviceId,userId from device")
    data1 = cur.fetchall()
    for i in range(0, len(data1)):
        data1[i] = {
            'deviceName': data1[i][0],
            'deviceId': data1[i][1],
            'userId': data1[i][2],
        }
    jsondata = {
        'file':data,
        'device':data1
    }
    return jsonify(jsondata)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9900')
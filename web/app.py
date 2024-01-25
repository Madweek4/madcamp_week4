from pymongo import MongoClient
from flask_cors import CORS
import certifi
from flask import Flask, render_template, send_file, request, redirect, url_for
import uuid, hashlib
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)
ca = certifi.where()
client = MongoClient('mongodb+srv://dlgudwls8184:NeTSWJRhf3bF7yIe@cluster0.escpqml.mongodb.net/', tlsCAFile = ca)
db = client['BlindHelper']
user_collection = db['User']


def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

@app.route('/')
def home():
    return render_template('start.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("login POST 들어옴")
        id = request.form['id']
        password = request.form['password']
        print(id)
        print(password)
        user = user_collection.find_one({'id' : id, 'password' : password})
        if user:
            hash_object = hashlib.sha256((id + password).encode())
            hex_dig = hash_object.hexdigest()
            return {'success': True, 'token': hex_dig}
        else:
            return {'success': False}
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("signup 들어옴")
        id = request.form['id']
        password = request.form['password']
        print(id)
        print(password)
        user = user_collection.find_one({'id' : id})
        if user:
            return {'success': False}
        else:
            user_collection.insert_one({'id' : id, 'password' : password, 'mac' : "", 'ispaid' : False, 'demo' : ""})
            hash_object = hashlib.sha256((id + password).encode())
            hex_dig = hash_object.hexdigest()
            return {'success': True, 'token': hex_dig}
    else:
        return render_template('signup.html')
    

@app.route('/download/blindhelper')
def downloadBlindHelper():
    return send_file('BlindHelper.zip', as_attachment=True)

@app.route('/download/license')
def downloadLicense():
    return send_file('BlindHelperLicense.exe', as_attachment=True)

@app.route('/download/demolicense')
def downloadDemoLicense():
    return send_file('Demo-BlindHelperLicense.exe', as_attachment=True)

@app.route('/certify', methods=['GET', 'POST'])
def certify():
    if request.method == 'POST':
        print("certify 들어옴")
        id = request.form['id']
        password = request.form['password']
        mac = request.form['mac']
        print(id)
        print(password)
        print(mac)
        user = user_collection.find_one({'id' : id, 'password' : password})
        if user:
            new_result = user_collection.update_one({'id' : id}, {'$set': {'mac': mac}})
            return {"success" : True}
        else: return {"success" : False}

@app.route('/getmac', methods=['GET', 'POST'])
def getMac():
    if request.method == 'POST':
        print("getmac 들어옴")
        mac = request.form['mac']
        print(mac)
        user = user_collection.find_one({'mac' : mac})
        if user == None:
            return {"success" : "nomac"} ##등록되지 않은 컴퓨터입니다
        if user['demo'] != "":
            current = datetime.now()
            stored_time = datetime.strptime(user['demo'], "%Y-%m-%d %H:%M:%S")
            if current - stored_time < timedelta(days=3):
                return {"success" : "True"} ## 프로그램을 시작합니다
            else: {"success" : "afterdemo"} ## 체험기간이 끝났습니다
        if user['ispaid']:
            return {"success" : "True"} ## 프로그램을 시작합니다
        else: return {"success" : "nomac"} ## 등록되지 않은 컴퓨터입니다

@app.route('/main', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        print("main POST 들어옴")
        token = request.form['token']
        userlist = user_collection.find()
        for user in userlist:
            hash_object = hashlib.sha256((user['id'] + user['password']).encode())
            hex_dig = hash_object.hexdigest()
            if hex_dig == token:
                return {"success" : True, "user" : {"id" : user['id'], "ispaid" : user['ispaid'], "demo" : user['demo']}}
        return {'success' : False}
    else:
        return render_template('main.html')
    
@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        print("pay 들어옴")
        token = request.form['token']
        userlist = user_collection.find()
        for user in userlist:
            hash_object = hashlib.sha256((user['id'] + user['password']).encode())
            hex_dig = hash_object.hexdigest()
            if hex_dig == token:
                user_collection.update_one({'id' : user['id']}, {'$set': {'ispaid': True}})
                return {"success" : True}
        return {"success" : False}
    
@app.route('/demostart', methods=['GET', 'POST'])
def demoStart():
    if request.method == 'POST':
        print("demostart 들어옴")
        token = request.form['token']
        userlist = user_collection.find()
        for user in userlist:
            hash_object = hashlib.sha256((user['id'] + user['password']).encode())
            hex_dig = hash_object.hexdigest()
            if hex_dig == token:
                current = datetime.now()
                user_collection.update_one({'id' : user['id']}, {'$set': {'demo': current.strftime("%Y-%m-%d %H:%M:%S")}})
                return {"success" : True}
        return {"success" : False}
    
@app.route('/detail', methods=['GET', 'POST'])
def detail():
    return render_template('detail.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

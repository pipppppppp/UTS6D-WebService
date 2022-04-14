# Helina Putri/6D/19090133
# Nirla Wahidatus Salam/6D/19090060
# Sri Mulyaningsih/6D/19090136
# Risma Nian Kupandang/6D/19090083

# import library
from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random, string, datetime

# Inisialisasi
dbfile = 'sqlite:///database/touring.db'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbfile
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# DATABASE
class Users(db.Model):
   username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
   password = db.Column(db.String(20), unique=False, nullable=False)
   token = db.Column(db.String(100), unique=False)

class Events(db.Model):
   event_name = db.Column(db.String(20), nullable=False, primary_key=True)
   event_creator = db.Column(db.String(20), nullable=False)
   event_start_time = db.Column(db.DateTime)
   event_end_time = db.Column(db.DateTime)
   event_start_lat = db.Column(db.String(20), nullable=False)
   event_finish_lat = db.Column(db.String(20), nullable=False)
   event_finish_lng = db.Column(db.String(20), nullable=False)
   created_at = db.Column(db.DateTime, default=datetime.datetime.now())

class Logs(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20))
   event_name = db.Column(db.String(20))
   log_lat = db.Column(db.String(20))
   log_lng = db.Column(db.String(20))
   created_at = db.Column(db.DateTime, default=datetime.datetime.now())

db.create_all()

# http://127.0.0.1:7007/api/v1/users/create
@app.route('/api/v1/users/create', methods=["POST"])
def registrasi():
   username = request.json['username']
   password = request.json['password']
   user = Users(username=username, password=password)
   db.session.add(user)
   db.session.commit()
   return make_response(jsonify({"msg": "registrasi sukses"}))

# http://127.0.0.1:7007/api/v1/users/login
@app.route('/api/v1/users/login', methods=["POST"])
def login():
   username = request.json['username']
   password = request.json['password']
   check = Users.query.filter_by(username=username, password=password).first()

   if check:
      token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
      Users.query.filter_by(username=username, password=password).update({'token': token})
      db.session.commit()
      return make_response(jsonify({"msg": "login sukses", "token": token}))
   return make_response(jsonify({"msg": "login failed"}))

# http://127.0.0.1:7007/api/v1/events/create
@app.route('/api/v1/events/create', methods=['POST'])
def event_create():
    token =  request.json['token']
    event_name = request.json['event_name']
    event_start_time = request.json['event_start_time']
    event_end_time = request.json['event_end_time']
    event_start_lat = request.json['event_start_lat']
    event_start_lng = request.json['event_start_lng']
    event_finish_lat = request.json['event_finish_lat']
    event_finish_lng = request.json['event_finish_lng']
    event_start_time = datetime.datetime.strptime(event_start_time, '%Y-%m-%d %H:%M') 
    event_end_time = datetime.datetime.strptime(event_end_time, '%Y-%m-%d %H:%M')
    
    user = Users.query.filter_by(token=token).first()
    if user:
        event = Events(event_creator=user.username, event_name=event_name, event_start_time=event_start_time, event_end_time=event_end_time, event_start_lat=event_start_lat, event_finish_lat=event_finish_lat, event_finish_lng=event_finish_lng)
        db.session.add(event)
        db.session.commit()
        return make_response(jsonify({"msg": "membuat event sukses"}))
    return make_response(jsonify({"msg":"membuat event gagal"}))

# http://127.0.0.1:7007/api/v1/events/log
@app.route("/api/v1/events/log", methods=["POST"])
def event_log():
    token = request.json['token']
    event_name = request.json['event_name']
    log_lat = request.json['log_lat']
    log_lng = request.json['log_lng']
    
    user = Users.query.filter_by(token=token).first()
    if user:
        logging = Logs(username=user.username, event_name=event_name, log_lat=log_lat, log_lng=log_lng)
        db.session.add(logging)
        db.session.commit()
        return make_response(jsonify({"msg":"Sukses mencatat posisi baru"}))
    return make_response(jsonify({"msg":"Token invalid"}))

# http://127.0.0.1:7007/api/v1/events/logs
if __name__ == '__main__':
   app.run(debug = True, port=7007)
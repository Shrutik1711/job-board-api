from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
import certifi
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=4000,
    database=os.getenv("DB_NAME"),
)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"ssl": {"ca": certifi.where()}}
}
db = SQLAlchemy(app)

class User(db.Model) :
    id = db.Column(db.Integer , primary_key = True)
    username =  db.Column(db.String(155) ,unique = True , nullable = False)
    password =  db.Column(db.String(155) , nullable = False)

class Job(db.Model) :
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(155) , nullable = False)
    company = db.Column(db.String(155) , nullable = False)
    location = db.Column(db.String(155) , nullable = False)
    description = db.Column(db.Text , nullable = False)


with app.app_context():
    db.create_all()



@app.route("/signup" , methods=["POST"])
def signup():
    data = request.json
    new_user = User(username = data ['username'], password = data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify ({"message" : " user register succesfully !!"})

@app.route("/login" , methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        return jsonify ({"message" : "user login succesfully !!"})
    else:
        return jsonify({"message" : "Invaild username and password !"}) ,401


@app.route("/jobs" , methods=["POST"])
def jobs ():
    data = request.json
    new_jobs = Job(
        title = data['title'] ,
        company = data['company'] ,
        location  = data['location'] ,
        description  = data['description']
    )
    db.session.add(new_jobs)
    db.session.commit()
    return jsonify ({'message' : "Job posted successfully!"})

@app.route("/jobs" , methods=["GET"])
def get_jobs():
    jobs = Job.query.all()
    result = [{"id" : j.id , "title": j.title, "company" : j.company , "location" : j.location , "description" : j.description} for j in jobs]
    return jsonify(result)


@app.route("/jobs/<int:id>" , methods=["PUT"])
def update_job(id):
    job = Job.query.get(id)
    if not job:
        return jsonify ({"message" : "job not found !!"}) , 404

    data = request.json
    job.title = data.get('title' , job.title)
    job.company = data.get('company' , job.company)
    job.location = data.get('location' , job.location)

    db.session.commit()
    return jsonify ({"message" : "job updated succesfully  !"})

@app.route("/jobs/<int:id>" , methods=["DELETE"])
def delete_job(id):
    job = Job.query.get(id)
    if not job :
        return jsonify ({"message" : "job not found !!"}) , 404

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message" : " job deleted succesfully !!"})

if __name__ == '__main__':
    app.run(debug=True)    

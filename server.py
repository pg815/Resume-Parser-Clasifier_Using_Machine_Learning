from flask import Flask, jsonify, redirect, request, Response, render_template, url_for, send_from_directory
import base64
import os
import json
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from resumeparse import resumeparse
from models import Model
import skillSuggestion
from db import *
import pandas as pd

app = Flask(__name__)  # initializing flask app
CORS(app)  # to avoid CORS errors

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def parse_file(filename):
    resume = resumeparse.read_file(filename)
    return resume


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/welcome', methods=['GET'])
def Welcome():
    return jsonify({'status': "success", 'message': "Welcome to Resume Parser API"})


@app.route('/UploadFile', methods=['POST'])
def UploadFile():
    error, message = None, None
    print("inside upload file")
    if request.method == 'POST':
        # print(request)
        # print(request.files)
        if 'resume' not in request.files:
            print('No file part')
            error = "No file part"
            return render_template('index.html', error=error)
        file = request.files['resume']
        if file.filename == '':
            print('No selected file')
            error = "No Selected File"
            return render_template('index.html', error=error)
        if file and allowed_file(file.filename):
            print("FileName is: "+str(file.filename))
            filename = secure_filename(file.filename)
            # path_on_cloud = "resumes/"+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # storage.child(path_on_cloud).put(
            #     os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resume = parse_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print(resume)
            if len(resume['grade_input']) > 0:
                model = Model()
                classifier = model.svm_classifier()
                prediction = classifier.predict([resume['grade_input']])
                # print(prediction)
            else:
                print("resume.grade_input is empty")

            if len(resume['skills']) > 0:
                suggestedSkills = skillSuggestion.suggestSkills(resume['skills'])
            else:
                print("resume.skills are empty")

        else:
            error = "Extension Not Allowed"
            return render_template('index.html', error=error)

    message = "Resume uploaded Successfully !!"
    success = True
    insert_record_to_db(resume, prediction[0])
    suggestions = get_related_suggestion(suggestedSkills)
    return render_template('index.html', error=error, message=message, success=success, skills = suggestions)


@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def validate_user():
    error = None
    username = request.form['username']
    password = request.form['password']

    if username == 'test' and password == 'test':
        return render_template('index.html')

    if username == 'admin' and password == 'admin':
        cv_record = Records()
        resumes = cv_record.get_records()
        return render_template('admin.html', resumes=resumes)

    error = "Invalid Username or Password !"
    return render_template('login.html', error=error)


@app.route('/logout', methods=['POST'])
def logout():
    return render_template('login.html')


def insert_record_to_db(data, grade):
    records = Records()
    designation = get_string(data['designition'])
    projects = get_string(data['projects'])
    degre = get_string(data['degree'])
    skills = get_string(data['skills'])
    accomplishments = get_string(data['accomplishments'])
    certifications = get_string(data['certifications'])
    records.insert_record(name=data['name'], phone=data['phone'], projects=projects,
                          skills=skills, linkedin=data['linkedin'], designation=designation,
                          degree=degre, certifications=certifications, accomplishments=accomplishments,
                          total_exp=str(data['total_exp']), grade=str(grade), email=data['email']
                          )
    print("Records inserted successfully")


def get_related_suggestion(skills):
    if skills:
        df = pd.DataFrame(skills)
        df = df.sort_values(['value'], ascending=False).head(3)
        return df.to_dict('records')
    else :
        return ""


def get_string(list_data):
    if list_data:
        text = ""
        for data in list_data:
            text = text + data + ", "
        return text
    else :
        return "None"


if __name__ == '__main__':
    record = Records()
    record.createTable()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

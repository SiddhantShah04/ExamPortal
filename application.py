from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 as db
import os
import csv


app = Flask(__name__)
app.secret_key = "E"

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Registration",methods=["POST","GET"])
def Registration():
    if(request.method == "POST"):
        Email = request.form.get("EMAIL")
        password = request.form.get("PASSWORD")
        if(Email == ""  or  password == ""):
            return("<h2>Are stupid or what</h2>?")
        con = db.connect('registration.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Registration VALUES (?,?)',(Email,password))
        con.commit()
        return redirect(url_for("Registration"))
    else:
        return render_template("index.html")


@app.route("/ProfessorZone",methods=["POST","GET"])
def ProfessorZone():
    if(request.method == "POST"):
        Email = request.form.get("Email")
        session['Email']=Email
        Password = request.form.get("Password")
        con = db.connect('registration.db')
        cur = con.cursor()
        rows = cur.execute("select email from Registration")
        E = rows.fetchall()
        rows = cur.execute("select password from Registration")
        P = rows.fetchall()
        for i in range(len(E)):
            if(E[i][0] == Email and P[i][0] == Password):
                return redirect(url_for('Email',Email=Email))
        return("<h1>invalid Email or password</h4>")
    else:
        return render_template("Professors.html")

@app.route('/Email/<string:Email>',methods=["POST","GET"])
def Email(Email):
    if('Email' in session):
        con = db.connect('Exam.db')
        cur = con.cursor()
        try:

            rows = cur.execute(f'select Branch,Sem,SubjectName  from "Exam" where Email = "{Email}" ')
            E = rows.fetchall()
        except:
            E=""

        return render_template("Professors.html",Email=Email,E=E)
    else:
        return render_template("index.html")

@app.route("/<string:Email>/Create_Question",methods=["POST","GET"])
def Create_Question(Email):
    if('Email' in session):
        return render_template("question.html",Email=Email)
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    if('Email' in session):
        session.pop('Email',None)
        return render_template("index.html")
    else:
        return("<h4>You already logout</h4>")

@app.route("/<string:Email>/uploader",methods=["POST","GET"])
def uploader(Email):
    if('Email' in session):
        f = request.files['file']
        f.save(os.path.join('UploadFiles',f.filename))
        Branch = request.form.get("Branch")
        Sem = request.form.get("Sem")
        #Subject = (request.form.get("Subject").replace(" ",""))
        Subject = (request.form.get("Subject"))
        con2 = db.connect('Exam.db')
        cur2 = con2.cursor()
        try:
            cur2.execute('create table Exam(Branch char(2),sem int(2),SubjectName varchar(100),FileName varchar(100),Email varchar(225))')
        except:
            print()
        cur2.execute('insert into Exam values(?,?,?,?,?)',(Branch,Sem,Subject,(f.filename),Email))
        con2.commit()
        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")
@app.route("/<string:r>/delete",methods=["POST","GET"])
def delete(r):
    if('Email' in session):
        Email = session['Email']
        con = db.connect('Exam.db')
        cur = con.cursor()
        rows = cur.execute(f'select FileName  from "Exam" where SubjectName = "{r}" ')
        E = rows.fetchone()
        R = E[0]
        cur.execute(f'DELETE FROM "Exam" WHERE SubjectName = "{r}" ')
        con.commit()
        os.remove(f'UploadFiles/{R}')
        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")
@app.route("/StudentZone",method=["POST","GET"])
def StudentZone():
    return("UnderProcess")
"""
@app.route("/<string:Email>/uploader",methods=["POST","GET"])
def upload(Email):
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join('UploadFiles',f.filename))
        with open(f'UploadFiles/{f.filename}', 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            row0 = next(csvreader)
            con2 = db.connect(f'{Email}.db')
            cur2 = con2.cursor()
            try:
                cur2.execute('create table Exam(Branch char(2),sem int(2),SubjectName varchar(100))')
            except:
                print()
            cur2.execute('insert into Exam values(?,?,?)',(row0[0],row0[1],row0[2]))
            con2.commit()
            try:
                os.mkdir(row0[0])
                path = os.path.join(row0[0],row0[1])
                os.mkdir(path)
                path2 = os.path.join(path,row0[2])
                path3 = os.mkdir(path2)
                #saving the subjects,semester and branch for future use or for retrive the information on professor page in .db file
            except:
                print()
            path4=os.path.join(row0[0],row0[1],row0[2])
            f.save(os.path.join(path4, f.filename))
        os.remove(f'UploadFiles/{f.filename}')
        return redirect(url_for('Email',Email=Email))
    else:
        return("Filed upload failed")

@app.route('/<string:Email>/<string:r>/delete',methods=["POST","GET"])
#@app.route('/Email/<string:Email>',methods=["POST","GET"])
def delete(Email,r):

    return redirect(url_for('Email',Email=Email))

"""
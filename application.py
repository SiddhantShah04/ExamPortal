from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,send_file
import os,shutil
import csv
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

engine = create_engine("postgres://axynzjdefwmyeo:e87f02858c1fbc56ea43154a07967f3d68c6e4ad7766daeee3eccc352380caa1@ec2-174-129-253-62.compute-1.amazonaws.com:5432/dcmaleb1aubmap")
db = scoped_session(sessionmaker(bind=engine))

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
        Password = request.form.get("PASSWORD")
        if(Email == ""  or  Password == ""):
            return("<h2>Are stupid or what</h2>?")
        try:
            db.execute('create table Registration(Email text,Password text)')
        except:
            db.rollback()
        #db.execute("insert into employee(name,address) values(:name,:address)" ,{"name":name,"address":address})

        db.execute("INSERT INTO Registration(Email,Password) VALUES(:Email,:Password)",{"Email":Email,"Password":Password})
        db.commit()

        return redirect(url_for("Registration"))
    else:
        return render_template("index.html")


@app.route("/ProfessorZone",methods=["POST","GET"])
def ProfessorZone():
    if(request.method == "POST"):
        Email = request.form.get("Email")
        session['Email']=Email
        Password = request.form.get("Password")

        rows = db.execute("select Email from Registration")
        E = rows.fetchall()
        rows = db.execute("select Password from Registration")
        P = rows.fetchall()
        for i in range(len(E)):
            if(E[i][0] == Email and P[i][0] == Password):
                return redirect(url_for('Email',Email=Email))
            else:
                return render_template("invalid.html")
    else:
        return render_template("Professors.html")

@app.route('/Email/<string:Email>',methods=["POST","GET"])
def Email(Email):
    if('Email' in session):

        rows = db.execute('select Branch,Sem,SubjectName  from "Exam" where email=(:email)',{"email":Email})
        E = rows.fetchall()

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
    db.commit()
    if('Email' in session):
        session.pop('Email',None)
        return redirect(url_for("index"))
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
        SubjectName = request.form.get("Subject")

        FileName = (f.filename)

        try:
            db.execute('insert into "Exam" (Branch,Sem,SubjectName,FileName,Email) values(:Branch,:Sem,:SubjectName,:FileName,:Email)',
                {"Branch":Branch,"Sem":Sem,"SubjectName":SubjectName,"FileName":FileName,"Email":Email})
            db.commit()
        except:
            db.rollback()
            #return("<h1>Exam with this Subject Name already exists</h1>")
        db.execute('create table ":SubjectName" (Question text,option1 text,option2 text,option3 text,option4 text,answer text,time SMALLINT)',
        {"SubjectName":SubjectName})
        db.commit()
        with open(f"UploadFiles/{FileName}", 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            for i in csvreader:
                db.execute('insert into ":SubjectName" values(:Question,:option1,:option2,:option3,:option4,:answer,:time)',
                {"SubjectName":SubjectName,"Question":i[0],"option1":i[1],"option2":i[2],"option3":i[3],"option4":i[4],"answer":i[5],"time":i[6]})
            db.commit()
        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")

@app.route("/<string:r>/delete",methods=["POST","GET"])
def delete(r):
    if('Email' in session):
        SubjectResult=f'{r}'+'Result'
        Email = session['Email']
        #db.execute("insert into ActiveSubject(Subject) values(:SubjectName)" ,{"SubjectName":r})
        rows = db.execute('select FileName  from "Exam" WHERE subjectname = (:subjectname)',{"subjectname":r})
        t=rows.fetchone()
        db.execute('DELETE FROM "Exam" WHERE subjectname = (:subjectname)',{"subjectname":r})
        db.execute('DELETE FROM "activesubject" WHERE "subject" =(:subjectname)',{"subjectname":r})
        db.execute('drop table ":subjectname"',{"subjectname":r})
        db.execute('drop table if exists ":SubjectResult"',{"SubjectResult":SubjectResult})
        os.remove(f'UploadFiles/{t[0]}')
        try:
            os.remove(f'Results/{r}.csv')
        except:
            pass
        db.commit()

        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")


@app.route("/StudentZone",methods=["POST","GET"])
def StudentZone():
    Branch = request.form.get("Branch")
    Roll = request.form.get("Roll")
    Subject = request.form.get("Subject")
    SubjectResult=f'{Subject}'+'Result'

    #rows = db.execute('select Branch,Sem,SubjectName  from "Exam" where email=(:email)',{"email":Email})
    rows = db.execute('select Question,option1,option2,option3,option4,time  from ":subject" ',{"subject":Subject})
    E = rows.fetchall()
    l=len(E)

    if(f'{Roll}' in session):
        return("<h1>already taken</h1>")
    session[f"{Roll}"] = 0
    s=1
    rows = E[session[f"{Roll}"]]
    return render_template("Paper.html",Subject=Subject,rows=rows,Roll=Roll,l=l,s=s)

@app.route("/<string:Subject>/<int:Roll>/Next",methods = ["POST","GET"])
def Next(Roll,Subject):
    s = f'{Subject}'
    SubjectResult=f'{Subject}'+'Result'

    rows = db.execute('select Question,option1,option2,option3,option4,time,answer  from ":subject" ',{"subject":s})
    E = rows.fetchall()
    l=len(E)
    QTaken = request.form.get("o")
    db.execute('create table if not exists ":SubjectName"("Roll" smallint not null,"Right" smallint not null)',{"SubjectName":SubjectResult})
    if(QTaken==E[session[f"{Roll}"]][6]):
        try:
            i=1
            db.execute('insert into ":SubjectName" ("Roll","Right") values(:Roll,:i)',{"SubjectName":SubjectResult,"Roll":Roll,"i":i})
            db.commit()
        except:
            db.rollback()
            rows = db.execute('select "Right" from ":SubjectName" where "Roll"=:Roll',{"SubjectName":SubjectResult,"Roll":Roll})
            i=(rows.fetchone())[0]
            i=i+1
            db.execute('UPDATE ":SubjectName" SET "Right" = :i WHERE "Roll" = :Roll',{"SubjectName":SubjectResult,"i":i,"Roll":Roll})
            db.commit()

    if(f"{Roll}" in session):
        session[f"{Roll}"] = session[f"{Roll}"]  + 1
        s=session[f"{Roll}"]+1
        try:
            rows = E[session[f"{Roll}"]]
        except:
            session.pop(f'{Roll}',None)
            return("<h1>Exam Done</h1>")
        return render_template("Paper.html",Subject=Subject,rows=rows,Roll=Roll,l=l,s=s)

@app.route("/<string:Email>/<string:Subject>/SeeResult",methods=["POST","GET"])
def SeeResult(Email,Subject):
    SubjectResult=f'{Subject}'+'Result'
    try:
        E=db.execute('select * from ":SubjectName" order by "Roll"',{"SubjectName":SubjectResult})
    except:
        return("<h1 style='text-align:center;'>Exam is not done<br>Yet!</h1>")
    R = E.fetchall()
    fields = ['Roll','Total right answer']
    rows = []
    for i in R:
        rows.append(i)

    filename = f"Results/{Subject}.csv"

    with open(filename,'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    path = f"{filename}"
    return send_file(path, as_attachment=True)

@app.route("/<string:Email>/<string:r>/Deploy",methods=["POST","GET"])
def Deploy(Email,r):
    try:
        db.execute("insert into ActiveSubject(Subject) values(:SubjectName)" ,{"SubjectName":r})
        db.commit()
    except:
        db.rollback()
        return("<h1 style='text-align:center;'>Already activated!</h1>")
    return redirect(url_for('Email',Email=Email))

# export DATABASE_URL=postgres://lrwrwexhxcpdec:0b3c469d7d2e697c0dcd67df8da24c8bbf62f5456d46733adcb141a9f7db84d4@ec2-54-83-9-36.compute-1.amazonaws.com:5432/db1hmn6a1q83g1
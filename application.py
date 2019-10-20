from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as db

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Registration",methods=["POST","GET"])
def Registration():
    if(request.method == "POST"):
        email = request.form.get("EMAIL")
        password = request.form.get("PASSWORD")
        con = db.connect('registration.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Registration VALUES (?,?)',(email,password))
        con.commit()
        return redirect(url_for("Registration"))
    else:
        return render_template("index.html")

@app.route("/ProfessorZone",methods=["POST","GET"])
def ProfessorZone():
    if(request.method == "POST"):
        Email = request.form.get("Email")
        Password = request.form.get("Password")
        con = db.connect('registration.db')
        cur = con.cursor()
        rows = cur.execute("select email from Registration")
        E = rows.fetchall()
        rows = cur.execute("select password from Registration")
        P = rows.fetchall()
        for i in range(len(E)):
            if(E[i][0] == Email and P[i][0] == Password):
                return redirect(url_for("ProfessorZone"))

        return("<h1>invalid Email or password</h4>")
    else:
        return render_template("Professors.html")

@app.route("/Create_Question",methods=["POST","GET"])
def Create_Question():
    return render_template("question.html")

@app.route("/Create_Paper",methods=["POST","GET"])
def Create_Paper():
    Branch = request.form.get("Branch")
    Sem = request.form.get("Sem")

    NumberOfQuestion = int(request.form.get("NumberOfQuestions"))
    Marks = request.form.get("Marks")
    SubjectName  = request.form.get("SubjectName")
    QuestionPaperCode = request.form.get("QuestionPaperCode")
    return render_template("Paper.html",Branch=Branch,Sem=Sem,NumberOfQuestion=NumberOfQuestion,Marks=Marks,QuestionPaperCode=QuestionPaperCode,SubjectName=SubjectName)



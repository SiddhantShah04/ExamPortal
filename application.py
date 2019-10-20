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

        if(email == ""  or  password == ""):
            return("<h2>Are stupid or what</h2>?")
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
                return redirect(url_for('Email',Email=Email))

        return("<h1>invalid Email or password</h4>")
    else:
        return render_template("Professors.html")


@app.route('/Email/<string:Email>')
def Email(Email):
    return render_template("Professors.html",Email=Email)

@app.route("/Create_Question/<string:Email>",methods=["POST","GET"])
def Create_Question(Email):
    return render_template("question.html",Email=Email)




@app.route("/Create_Paper/<string:Email>",methods=["POST","GET"])
def Create_Paper(Email):

    Branch = request.form.get("Branch")
    Sem = request.form.get("Sem")
    NumberOfQuestion = int(request.form.get("NumberOfQuestions"))
    Marks = request.form.get("Marks")
    SubjectName  = request.form.get("SubjectName")
    QuestionPaperCode = request.form.get("QuestionPaperCode")
    try:
        con2 = db.connect(f'{Email}.db')
        cur2 = con2.cursor()
        cur2.execute('create table Paper (Branch charr(2),sem int(2),NumberofQuestion int(4),Marks int(5),SubjectName varchar(100),QuestionPaperCode int(6))')

    except:
        print()
    cur2.execute('insert into Paper values(?,?,?,?,?,?)',(Branch,Sem,NumberOfQuestion,Marks,SubjectName,QuestionPaperCode))
    con2.commit()

    return render_template("Paper.html",Email=Email,Branch=Branch,Sem=Sem,NumberOfQuestion=NumberOfQuestion,Marks=Marks,QuestionPaperCode=QuestionPaperCode,SubjectName=SubjectName)



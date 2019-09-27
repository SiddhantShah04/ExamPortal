from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as db

#cur.execute('create table Registration(Email varchar(225),Password varchar(50))')
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





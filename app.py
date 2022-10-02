import cx_Oracle
import os, sys
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values

trim_results_to = 10


app = Flask(__name__)
if os.path.exists(os.getenv("CONFIG_FILE", ".env")):
    config = dotenv_values(".env")

    # if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get("PWD")+"/instantclient_19_8")


    dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XE")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://sysdba:demopass@' + dsn

    # DIALECT = 'oracle'
    # SQL_DRIVER = 'cx_oracle'
    # USERNAME = 'your_username' #enter your username
    # PASSWORD = 'your_password' #enter your password
    # HOST = 'subdomain.domain.tld' #enter the oracle db host url
    # PORT = 1521 # enter the oracle port number
    # SERVICE = 'your_oracle_service_name' # enter the oracle db service name
    # ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE


    try:
      # app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
      app.config["SECRET_KEY"] = config["SECRET_KEY"]
    except KeyError as e:
        print(f"ERROR: Missing configuration {e}")
        sys.exit(1)



else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.sqlite3"
    app.config["SECRET_KEY"] = "random-string"

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column("student_id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin


@app.route("/")
def show_all():
    _students = students.query.all()
    _count = len(_students)
    return render_template("show_all.html", students=_students[-trim_results_to:], count=_count)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        if (
            not request.form["name"]
            or not request.form["city"]
            or not request.form["addr"]
        ):
            flash("Please enter all the fields", "error")
        else:
            student = students(
                request.form["name"],
                request.form["city"],
                request.form["addr"],
                request.form["pin"],
            )

            db.session.add(student)
            db.session.commit()
            flash("Record was successfully added")
            return redirect(url_for("show_all"))
    return render_template("new.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

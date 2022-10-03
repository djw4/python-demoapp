import os, sys
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values

trim_results_to = 10
config_file = ".env"

app = Flask(__name__)
if os.path.exists(os.getenv("CONFIG_FILE", config_file)):
    config = dotenv_values(config_file)
    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
        app.config["SECRET_KEY"] = config["SECRET_KEY"]
    except KeyError as e:
        print(f"ERROR: Missing configuration {e}")
        sys.exit(1)

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
    return render_template(
        "show_all.html", students=_students[-trim_results_to:], count=_count
    )


@app.route("/students", methods=["GET"])
def ids():
    _ids = [s.id for s in students.query.all()]
    return {"student_ids": _ids}


@app.route("/students/<int:id>", methods=["GET", "POST"])
def update(id):
    student = students.query.filter_by(id=id).first()

    r = {
        "id": id,
        "attributes": {
            "name": student.name,
            "city": student.city,
            "addr": student.addr,
            "pin": student.pin,
        },
    }

    if request.method == "GET":
        return r

    if request.method == "POST":
        r["updated"] = {}

        for attr in ["name", "city", "addr", "pin"]:
            if getattr(student, attr) != request.form[attr]:
                setattr(student, attr, request.form[attr])
                r["updated"][attr] = getattr(student, attr)

        db.session.commit()
        return r


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

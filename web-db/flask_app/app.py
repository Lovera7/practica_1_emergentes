from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

app.config["MYSQL_HOST"] = "web-db-service"
app.config["MYSQL_USER"] = "example_user"
app.config["MYSQL_PASSWORD"] = "mysql"
app.config["MYSQL_DB"] = "example"
app.config["MYSQL_PORT"] = 8306

mysql = MySQL(app)


@app.route("/", methods=["GET"])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, first_name, last_name, city, semester FROM student")
    data = cursor.fetchall()
    return json.dumps(data)


@app.route("/studentlist", methods=["GET"])
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, first_name, last_name, city, semester FROM student")
    data = cursor.fetchall()
    return render_template("list.html", students=data)


@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        city = request.form["city"]
        semester = request.form["semester"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO student (first_name, last_name, city, semester) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, city, semester),
        )
        mysql.connection.commit()
        cursor.close()

        return redirect("/studentlist")

    return render_template("add_student.html")


@app.route("/update_student/<int:id>", methods=["GET", "POST"])
def update_student(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
    student = cursor.fetchone()

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        city = request.form["city"]
        semester = request.form["semester"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE student SET first_name=%s, last_name=%s, city=%s, semester=%s WHERE id=%s",
            (first_name, last_name, city, semester, id),
        )
        mysql.connection.commit()
        cursor.close()

        return redirect("/studentlist")

    return render_template("update_student.html", student=student)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)

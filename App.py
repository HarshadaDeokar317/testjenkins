from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

#con = sqlite3.connect("Employees.db")
#Database opened successfully


#con.execute("create table Employee_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, address TEXT NOT NULL)")
#Table created successfully

@app.route("/")
def index():
    return render_template("index.html");


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/details", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("Employees.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employee_Data (name, email, address) values (?,?,?)", (name, email, address))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            return render_template("duplicate.html")

    return render_template("success.html", msg=msg)
    con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("Employees.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employee_Data")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


#Update-----------------------------------------------------------

@app.route("/Update")
def update():
    con = sqlite3.connect("Employees.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employee_Data")
    rows = cur.fetchall()
    return render_template("update.html", rows=rows)


@app.route("/updaterecord", methods=["POST", "GET"])
def updaterecod():
    msg = "msg"
    if request.method == "POST":
        try:
            id = request.form["id"]

            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("Employees.db") as con:
                cur = con.cursor()
                cur.execute("update Employee_Data set name=?,email=?,address=? where id=?",
                            (name, email, address, id))

                con.commit()
                msg = "Employee successfully updated"
        except:
            con.rollback()
            msg = "We can not update the employee."
        finally:
            return render_template("update_record.html", msg=msg)
            con.close()



#Delete---------------------------------------------------------
@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("Employees.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employee_Data where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)





if __name__ == '__main__':
    app.run(debug=True, port=7070, host='0.0.0.0')

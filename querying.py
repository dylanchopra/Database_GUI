from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/query", methods = ["POST", "GET"])
def query():
    con = sqlite3.connect("flowers2019.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("SELECT * FROM flowers ORDER BY comname")  
    rows = cur.fetchall()  
    return render_template("viewflowers.html",rows = rows)

@app.route("/viewsightings", methods = ["POST", "GET"])
def viewsightings():
    iname = request.form["name"]
    con = sqlite3.connect("flowers2019.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("SELECT person, location, sighted FROM sightings WHERE name = (?) ORDER BY sighted DESC", (iname, ))
    rows = cur.fetchmany(10)
    return render_template("viewsightings.html", rows = rows) 

@app.route("/updateflower")
def update():
    return render_template("update.html")

@app.route("/udetails", methods = ["POST", "GET"])
def udetails():
    m = "."
    if request.method == "POST":
        try:
            newg = request.form["newgenus"]  
            news = request.form["newspecies"]
            newn = request.form["newname"]
            oldn = request.form["oldname"] 
            with sqlite3.connect("flowers2019.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE flowers SET genus = ?, species = ?, comname = ? WHERE comname = ?", (newg, news, newn, oldn))
                con.commit()
                m = "Flower information updated successfully"
        except:
            con.rollback()
            m = "We could not update the flower information"
        finally:
            return render_template("success.html", m=m)
            con.close()


@app.route("/insert", methods = ["POST", "GET"])
def insert():
    return render_template("insert.html")

@app.route("/details", methods = ["GET", "POST"])
def details():
    m = "."  
    if request.method == "POST":  
        try:  
            name = request.form["name"]  
            person = request.form["person"]  
            location = request.form["location"]  
            sighted = request.form["sighted"]
            with sqlite3.connect("flowers2019.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Sightings (name, person, location, sighted) values (?,?,?,?)",(name,person,location,sighted))  
                con.commit()  
                m = "Sighting successfully added to table"  
        except:  
            con.rollback()  
            m = "We can not add the sighting to the list"  
        finally:  
            return render_template("success.html",m = m)  
            con.close()  


if __name__ == "__main__":  
    app.run(port=5000, debug = True)  



from flask import Flask, render_template 
from database import cur

app= Flask(__name__)

@app.route("/")
def index():
    name = "Peter"
    return render_template("index.html", myname=name)

@app.route("/about")
def about():
    return "This is where the about statement is supposed to display"

@app.route("/contact")
def contact():
    return "This is where the contact statement should display"

@app.route("/theproducts")
def theproducts():
    cur.execute("select * FROM theproducts")
    theproducts = cur.fetchall()
    print(theproducts)
    return render_template("theproducts.html", myproducts=theproducts)

app.run()
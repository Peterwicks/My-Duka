from flask import Flask, render_template, request
from database import cur
from datetime import datetime


app= Flask(__name__)

# Define a custom filter- this will be used to format the date(should be done after importing datetime)
@app.template_filter('strftime')
def format_datetime(value, format="%B %d, %Y"):
    return value.strftime(format)

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

@app.route("/theproducts", methods=["GET", "POST"])
def theproducts():
    cur.execute("select * FROM theproducts")
    if request.method=="GET":
        theproducts = cur.fetchall()
    #print(theproducts)
        return render_template("theproducts.html", myproducts=theproducts)
    else:
        name=request.form["pname"]
        buying_price=request.form["BP"]
        selling_price=request.form["SP"]
        stock_quantity=request.form["ST"]
        print(name, buying_price, selling_price, stock_quantity)

@app.route("/thesales")
def thesales():
    cur.execute("select thesales.id, theproducts.name, thesales.quantity, thesales.created_at FROM thesales join theproducts on theproducts.id=thesales.pid")
   
    thesales=cur.fetchall()
    print(thesales)
    return render_template("thesales.html", thesales=thesales, theproducts=cur.fetchall())

app.run(debug=True)
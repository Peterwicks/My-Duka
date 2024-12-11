from flask import Flask, render_template, request, redirect
from database import conn, cur
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
        cur.execute("SELECT *FROM theproducts order by id desc")
        theproducts = cur.fetchall()
        print(theproducts)
        return render_template("theproducts.html", myproducts=theproducts)
    else:
        name=request.form["pname"]
        buying_price=request.form["BP"]
        selling_price=request.form["SP"]
        stock_quantity=request.form["ST"]
        print(name, buying_price, selling_price, stock_quantity)
        if selling_price < buying_price:
            return "Selling price should be greater than buying price"
        query="insert into theproducts(name,buying_price,selling_price,stock_quantity) "\
        "values('{}',{},{},{})".format(name,buying_price,selling_price,stock_quantity)
        cur.execute(query)
        conn.commit()
        return redirect("/theproducts")
    

@app.route("/thesales", methods=["GET", "POST"])
def thesales():
    if request.method=="POST":
        pid = request.form["pid"]
        amount = request.form["amount"]
        print(pid, amount)
        query_1= "insert into thesales(pid,quantity, created_at)" \
            "values('{}',{}, {})".format(pid,amount, 'now()')
        cur.execute(query_1)
        return redirect("thesales")
    
    else:
        cur.execute("select * from theproducts")
        theproducts= cur.fetchall()
        cur.execute("select thesales.id, theproducts.name, thesales.quantity, thesales.created_at"\
                     "FROM thesales join theproducts on theproducts.id=thesales.pid")
        thesales=cur.fetchall()
        
        return render_template("thesales.html", theproducts=theproducts, thesales=thesales)
@app.route("/dashboard")
def dashboard():
    cur.execute("select sum(p.selling_price * s.quantity) as sales,"\
                "s.created_at from thesales as s join theproducts as p on p.id =s.pid group by s.created_at;")
    daily_sales = cur.fetchall()
    #print(daily_sales)
    x = [i[1].strftime('%d %m %Y') for i in daily_sales if float(i[0]) > 90000000]
    y = [float(i[0]) for i in daily_sales if float(i[0]) > 90000000]
    for i in daily_sales:
       
        return render_template("dashboard.html", x=x, y=y)

#task 2: sales per product
#x axis product name
#y axis sale
#bar graph group by product name
@app.route("/dashboard_2")
def dashboard_2(): 
    cur.execute("select name as product_name, SUM(selling_price) AS total_sales from theproducts group by name ")
    sales_per_product =cur.fetchall()
    
    
    x=[s[0] for s in sales_per_product]
    y=[float(s[1]) for s in sales_per_product]
    for s in sales_per_product:
        return render_template("dashboard_2.html", x=x, y=y)
    
@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        name= request.form["Name"]
        email=request.form["Email"]
        password= request.form["Password"]
        query= "insert into users (name, email, password) values ('{}', '{}', '{}')".format(name,email,password)
        cur.execute(query)
        conn.commit()
        return redirect ("/dashboard")


app.run(debug=True)
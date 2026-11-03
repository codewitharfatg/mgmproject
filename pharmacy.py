
                    # =====================================================
# MEDICAL PHARMACY MANAGEMENT SYSTEM
# PART 1 - CORE SYSTEM + LOGIN + DASHBOARD
# Flask + SQLite3
# =====================================================


from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from datetime import datetime
import os
import shutil


app = Flask(__name__)

app.secret_key = "pharmacy_secure_key_2026"


DATABASE = "pharmacy.db"



# ================= DATABASE =================


def db():

    return sqlite3.connect(DATABASE)



def create_database():

    conn = db()

    cur = conn.cursor()



    # USERS

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT

    )
    """)



    # MEDICINES

    cur.execute("""
    CREATE TABLE IF NOT EXISTS medicines(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        category TEXT,

        batch TEXT,

        purchase_price REAL,

        selling_price REAL,

        quantity INTEGER,

        expiry TEXT

    )
    """)




    # SUPPLIERS

    cur.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        phone TEXT,

        address TEXT

    )
    """)




    # PURCHASE

    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        supplier TEXT,

        medicine TEXT,

        quantity INTEGER,

        price REAL,

        date TEXT

    )
    """)




    # CUSTOMERS

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        age INTEGER,

        phone TEXT,

        address TEXT

    )
    """)




    # SALES

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        bill_no TEXT,

        customer TEXT,

        medicine TEXT,

        quantity INTEGER,

        price REAL,

        total REAL,

        date TEXT

    )
    """)



    # DEFAULT ADMIN


    cur.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )


    if cur.fetchone() is None:


        cur.execute(

        """

        INSERT INTO users(username,password)

        VALUES(?,?)

        """,

        ("admin","admin")

        )



    conn.commit()

    conn.close()





create_database()






# ================= LOGIN PAGE =================



login_page = """

<!DOCTYPE html>

<html>

<head>


<title>
Pharmacy Login
</title>


<style>


body{

margin:0;

font-family:Arial;

background:linear-gradient(135deg,#009879,#004d40);

height:100vh;

display:flex;

align-items:center;

justify-content:center;

}



.login{

background:white;

width:350px;

padding:35px;

border-radius:15px;

box-shadow:0 0 20px #333;

}



h2{

text-align:center;

color:#009879;

}



input{

width:100%;

padding:12px;

margin:10px 0;

border-radius:5px;

border:1px solid #ccc;

}



button{

width:100%;

padding:12px;

background:#009879;

color:white;

border:0;

border-radius:5px;

font-size:16px;

}



.error{

color:red;

text-align:center;

}



</style>


</head>



<body>



<div class="login">


<h2>
Medical Pharmacy
</h2>



{% if error %}

<p class="error">
{{error}}
</p>

{% endif %}



<form method="post">


<input name="username"
placeholder="Username">


<input type="password"
name="password"
placeholder="Password">



<button>
Login
</button>



</form>



<center>

<br>

Default Login

<br>

<b>
admin / admin
</b>


</center>


</div>


</body>


</html>

"""






# ================= LOGIN =================


@app.route("/", methods=["GET","POST"])

def login():


    if request.method=="POST":


        username=request.form["username"]

        password=request.form["password"]



        conn=db()

        cur=conn.cursor()



        cur.execute(

        """

        SELECT * FROM users

        WHERE username=? AND password=?

        """,

        (username,password)

        )


        user=cur.fetchone()


        conn.close()



        if user:


            session["user"]=username


            return redirect("/dashboard")



        else:


            return render_template_string(

                login_page,

                error="Invalid Login"

            )



    return render_template_string(

        login_page,

        error=""

    )







# ================= DASHBOARD =================



dashboard_page = """

<!DOCTYPE html>

<html>

<head>


<title>
Dashboard
</title>


<style>


body{

margin:0;

font-family:Arial;

background:#f1f5f4;

}



.header{

background:#009879;

color:white;

padding:20px;

font-size:24px;

}



.menu{

background:#004d40;

width:220px;

height:100vh;

position:fixed;

top:0;

left:0;

padding-top:80px;

}



.menu a{

display:block;

color:white;

padding:15px;

text-decoration:none;

}



.menu a:hover{

background:#009879;

}



.content{

margin-left:240px;

padding:30px;

}



.card{

display:inline-block;

background:white;

padding:25px;

margin:15px;

width:200px;

border-radius:15px;

box-shadow:0 0 10px #ccc;

text-align:center;

}



</style>



</head>


<body>


<div class="menu">


<a href="/dashboard">
Dashboard
</a>


<a href="/medicines">
Medicines
</a>


<a href="/suppliers">
Suppliers
</a>


<a href="/purchase">
Purchase
</a>


<a href="/sales">
Sales
</a>


<a href="/reports">
Reports
</a>


<a href="/backup">
Backup
</a>


<a href="/logout">
Logout
</a>


</div>




<div class="content">


<div class="header">

Medical Pharmacy Management System

</div>




<h2>
Welcome {{user}}
</h2>



<div class="card">

<h1>
{{medicine}}
</h1>

Medicines

</div>



<div class="card">

<h1>
₹ {{sales}}
</h1>

Sales

</div>



</div>



</body>

</html>

"""





@app.route("/dashboard")

def dashboard():


    if "user" not in session:

        return redirect("/")



    conn=db()

    cur=conn.cursor()



    cur.execute(
        "SELECT COUNT(*) FROM medicines"
    )

    medicine=cur.fetchone()[0]



    cur.execute(
        "SELECT SUM(total) FROM sales"
    )


    sales=cur.fetchone()[0]


    if sales is None:

        sales=0



    conn.close()



    return render_template_string(

        dashboard_page,

        user=session["user"],

        medicine=medicine,

        sales=sales

    )






# ================= LOGOUT =================


@app.route("/logout")

def logout():

    session.clear()

    return redirect("/")



# ================= PART 1 END =================
# =====================================================
# PART 2
# MEDICINE INVENTORY + SUPPLIER MANAGEMENT
# =====================================================



# ================= MEDICINE PAGE =================


medicine_page = """

<!DOCTYPE html>

<html>

<head>

<title>
Medicine Inventory
</title>


<style>


body{

font-family:Arial;

background:#f1f5f4;

}


.box{

background:white;

margin:30px;

padding:25px;

border-radius:15px;

box-shadow:0 0 10px #ccc;

}



input{

padding:10px;

margin:5px;

border:1px solid #ccc;

border-radius:5px;

}



button{

background:#009879;

color:white;

padding:10px 20px;

border:0;

border-radius:5px;

}



table{

width:100%;

border-collapse:collapse;

margin-top:20px;

}



th{

background:#009879;

color:white;

}



td,th{

padding:10px;

border:1px solid #ddd;

text-align:center;

}



.low{

color:red;

font-weight:bold;

}



a{

color:#009879;

text-decoration:none;

}



</style>


</head>



<body>



<div class="box">


<a href="/dashboard">
← Dashboard
</a>



<h2>
Medicine Inventory
</h2>




<form method="post">



<input name="name"
placeholder="Medicine Name"
required>



<input name="category"
placeholder="Category"
required>



<input name="batch"
placeholder="Batch No"
required>



<input name="purchase_price"
placeholder="Purchase Price"
type="number"
step="0.01"
required>



<input name="selling_price"
placeholder="Selling Price"
type="number"
step="0.01"
required>



<input name="quantity"
placeholder="Quantity"
type="number"
required>



<input name="expiry"
type="date"
required>



<button>
Add Medicine
</button>



</form>





<form method="get">


<input name="search"
placeholder="Search Medicine">


<button>
Search
</button>


</form>





<table>


<tr>

<th>Name</th>

<th>Category</th>

<th>Batch</th>

<th>Buy Price</th>

<th>Sell Price</th>

<th>Stock</th>

<th>Expiry</th>


</tr>




{% for m in medicines %}


<tr>


<td>{{m[1]}}</td>

<td>{{m[2]}}</td>

<td>{{m[3]}}</td>

<td>{{m[4]}}</td>

<td>{{m[5]}}</td>



<td>


{% if m[6] < 10 %}


<span class="low">

{{m[6]}} LOW

</span>


{% else %}


{{m[6]}}


{% endif %}



</td>



<td>{{m[7]}}</td>


</tr>


{% endfor %}



</table>



</div>



</body>


</html>


"""







@app.route("/medicines", methods=["GET","POST"])

def medicines():


    if "user" not in session:

        return redirect("/")



    conn=db()

    cur=conn.cursor()



    if request.method=="POST":


        cur.execute(

        """

        INSERT INTO medicines

        (

        name,

        category,

        batch,

        purchase_price,

        selling_price,

        quantity,

        expiry

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

        request.form["name"],

        request.form["category"],

        request.form["batch"],

        request.form["purchase_price"],

        request.form["selling_price"],

        request.form["quantity"],

        request.form["expiry"]

        )

        )


        conn.commit()




    search=request.args.get("search","")



    if search:


        cur.execute(

        """

        SELECT * FROM medicines

        WHERE name LIKE ?

        """,

        ("%"+search+"%",)

        )


    else:


        cur.execute(

        """

        SELECT * FROM medicines

        ORDER BY id DESC

        """

        )



    medicines=cur.fetchall()



    conn.close()



    return render_template_string(

        medicine_page,

        medicines=medicines

    )








# =====================================================
# SUPPLIER MANAGEMENT
# =====================================================



supplier_page = """

<html>


<head>


<title>
Suppliers
</title>



<style>


body{

font-family:Arial;

background:#f1f5f4;

}


.box{

background:white;

margin:30px;

padding:25px;

border-radius:15px;

}



input{

padding:10px;

margin:5px;

}



button{

background:#009879;

color:white;

padding:10px;

border:0;

}



table{

width:100%;

border-collapse:collapse;

}



td,th{

padding:10px;

border:1px solid #ddd;

}



th{

background:#009879;

color:white;

}



</style>


</head>



<body>



<div class="box">


<a href="/dashboard">
Dashboard
</a>



<h2>
Supplier Management
</h2>




<form method="post">



<input name="name"
placeholder="Supplier Name"
required>



<input name="phone"
placeholder="Phone"
required>



<input name="address"
placeholder="Address"
required>



<button>
Save Supplier
</button>



</form>






<table>


<tr>

<th>Name</th>

<th>Phone</th>

<th>Address</th>


</tr>



{% for s in suppliers %}


<tr>

<td>{{s[1]}}</td>

<td>{{s[2]}}</td>

<td>{{s[3]}}</td>


</tr>


{% endfor %}



</table>



</div>



</body>


</html>


"""






@app.route("/suppliers", methods=["GET","POST"])

def suppliers():


    if "user" not in session:

        return redirect("/")



    conn=db()

    cur=conn.cursor()



    if request.method=="POST":


        cur.execute(

        """

        INSERT INTO suppliers

        (name,phone,address)

        VALUES(?,?,?)

        """,

        (

        request.form["name"],

        request.form["phone"],

        request.form["address"]

        )

        )


        conn.commit()




    cur.execute(

    """

    SELECT * FROM suppliers

    ORDER BY id DESC

    """

    )


    suppliers=cur.fetchall()



    conn.close()



    return render_template_string(

        supplier_page,

        suppliers=suppliers

    )



# ================= PART 2 END =================
# =====================================================
# PART 3
# PURCHASE MANAGEMENT + STOCK UPDATE
# =====================================================



purchase_page = """

<!DOCTYPE html>

<html>


<head>


<title>
Purchase Management
</title>



<style>


body{

font-family:Arial;

background:#f1f5f4;

}



.box{

background:white;

margin:30px;

padding:25px;

border-radius:15px;

box-shadow:0 0 10px #ccc;

}



select,input{

padding:10px;

margin:5px;

border-radius:5px;

border:1px solid #ccc;

}



button{

background:#009879;

color:white;

padding:10px 20px;

border:0;

border-radius:5px;

}



table{

width:100%;

border-collapse:collapse;

margin-top:20px;

}



th{

background:#009879;

color:white;

}



td,th{

padding:10px;

border:1px solid #ddd;

text-align:center;

}



a{

color:#009879;

text-decoration:none;

}



</style>


</head>



<body>



<div class="box">



<a href="/dashboard">
← Dashboard
</a>



<h2>
Purchase Medicines
</h2>




<form method="post">



<label>
Supplier
</label>



<select name="supplier" required>


<option value="">
Select Supplier
</option>


{% for s in suppliers %}


<option value="{{s[1]}}">

{{s[1]}}

</option>


{% endfor %}



</select>




<br>




<label>
Medicine
</label>



<select name="medicine" required>



<option value="">
Select Medicine
</option>



{% for m in medicines %}



<option value="{{m[1]}}">

{{m[1]}}

</option>



{% endfor %}



</select>




<br>



<input

type="number"

name="quantity"

placeholder="Quantity"

required>



<input

type="number"

step="0.01"

name="price"

placeholder="Purchase Price"

required>




<button>

Save Purchase

</button>



</form>







<h2>
Purchase History
</h2>



<table>



<tr>

<th>Supplier</th>

<th>Medicine</th>

<th>Quantity</th>

<th>Price</th>

<th>Date</th>


</tr>





{% for p in purchases %}



<tr>


<td>
{{p[1]}}
</td>


<td>
{{p[2]}}
</td>


<td>
{{p[3]}}
</td>


<td>
{{p[4]}}
</td>


<td>
{{p[5]}}
</td>



</tr>



{% endfor %}




</table>





</div>



</body>


</html>



"""









@app.route("/purchase", methods=["GET","POST"])

def purchase():


    if "user" not in session:

        return redirect("/")



    conn=db()

    cur=conn.cursor()





    if request.method=="POST":



        supplier=request.form["supplier"]

        medicine=request.form["medicine"]

        quantity=int(request.form["quantity"])

        price=float(request.form["price"])





        # save purchase record


        cur.execute(

        """

        INSERT INTO purchases

        (supplier,medicine,quantity,price,date)

        VALUES(?,?,?,?,?)

        """,

        (

        supplier,

        medicine,

        quantity,

        price,

        datetime.now().strftime("%Y-%m-%d")

        )

        )






        # increase stock


        cur.execute(

        """

        UPDATE medicines

        SET quantity = quantity + ?

        WHERE name=?

        """,

        (

        quantity,

        medicine

        )

        )





        conn.commit()






    # load suppliers


    cur.execute(

    """

    SELECT * FROM suppliers

    ORDER BY name

    """

    )


    suppliers=cur.fetchall()







    # load medicines


    cur.execute(

    """

    SELECT * FROM medicines

    ORDER BY name

    """

    )


    medicines=cur.fetchall()






    # purchase list


    cur.execute(

    """

    SELECT * FROM purchases

    ORDER BY id DESC

    """

    )


    purchases=cur.fetchall()





    conn.close()





    return render_template_string(

        purchase_page,

        suppliers=suppliers,

        medicines=medicines,

        purchases=purchases

    )





# ================= PART 3 END =================
# =====================================================
# PART 4
# CUSTOMER + SALES + BILLING SYSTEM
# =====================================================



sales_page = """

<!DOCTYPE html>

<html>


<head>


<title>
Sales Billing
</title>



<style>


body{

font-family:Arial;

background:#f1f5f4;

}



.box{

background:white;

margin:30px;

padding:25px;

border-radius:15px;

box-shadow:0 0 10px #ccc;

}



input,select{

padding:10px;

margin:5px;

border-radius:5px;

border:1px solid #ccc;

}



button{

background:#009879;

color:white;

padding:12px 25px;

border:0;

border-radius:5px;

}



table{

width:100%;

border-collapse:collapse;

margin-top:20px;

}



th{

background:#009879;

color:white;

}



td,th{

padding:10px;

border:1px solid #ddd;

text-align:center;

}



.bill{

background:#e8fff7;

padding:15px;

border-left:5px solid #009879;

}



a{

color:#009879;

text-decoration:none;

}


</style>


</head>



<body>



<div class="box">



<a href="/dashboard">

← Dashboard

</a>



<h2>
Customer Billing
</h2>




<form method="post">



<h3>
Customer Details
</h3>



<input

name="customer"

placeholder="Customer Name"

required>




<input

type="number"

name="age"

placeholder="Age"

required>




<input

name="phone"

placeholder="Phone Number"

required>




<input

name="address"

placeholder="Address"

required>






<h3>
Medicine Sale
</h3>



<select name="medicine" required>


<option>

Select Medicine

</option>



{% for m in medicines %}


<option value="{{m[1]}}">

{{m[1]}} 
(Stock {{m[6]}})

</option>


{% endfor %}



</select>





<input

type="number"

name="quantity"

placeholder="Quantity"

required>





<button>

Generate Bill

</button>



</form>





{% if message %}


<div class="bill">

<h3>

{{message}}

</h3>


</div>


{% endif %}







<h2>
Sales History
</h2>




<table>


<tr>


<th>
Bill No
</th>


<th>
Customer
</th>


<th>
Medicine
</th>


<th>
Quantity
</th>


<th>
Total
</th>


<th>
Date
</th>



</tr>





{% for s in sales %}



<tr>


<td>

{{s[1]}}

</td>


<td>

{{s[2]}}

</td>


<td>

{{s[3]}}

</td>


<td>

{{s[4]}}

</td>


<td>

₹ {{s[6]}}

</td>


<td>

{{s[7]}}

</td>



</tr>



{% endfor %}




</table>




</div>



</body>


</html>


"""









@app.route("/sales", methods=["GET","POST"])

def sales():


    if "user" not in session:

        return redirect("/")



    conn=db()

    cur=conn.cursor()



    message=""





    if request.method=="POST":



        customer=request.form["customer"]

        age=request.form["age"]

        phone=request.form["phone"]

        address=request.form["address"]


        medicine=request.form["medicine"]

        quantity=int(request.form["quantity"])





        # customer save


        cur.execute(

        """

        INSERT INTO customers

        (name,age,phone,address)

        VALUES(?,?,?,?)

        """,

        (

        customer,

        age,

        phone,

        address

        )

        )







        # check medicine stock



        cur.execute(

        """

        SELECT selling_price,quantity

        FROM medicines

        WHERE name=?

        """,

        (medicine,)

        )



        item=cur.fetchone()





        if item is None:



            message="Medicine not found"





        elif item[1] < quantity:



            message="Not enough stock"






        else:



            price=item[0]

            total=price*quantity




            bill="BILL-"+datetime.now().strftime("%Y%m%d%H%M%S")






            # save sale



            cur.execute(

            """

            INSERT INTO sales

            (

            bill_no,

            customer,

            medicine,

            quantity,

            price,

            total,

            date

            )

            VALUES(?,?,?,?,?,?,?)

            """,

            (

            bill,

            customer,

            medicine,

            quantity,

            price,

            total,

            datetime.now().strftime("%Y-%m-%d")

            )

            )







            # reduce stock



            cur.execute(

            """

            UPDATE medicines

            SET quantity=quantity-?

            WHERE name=?

            """,

            (

            quantity,

            medicine

            )

            )





            conn.commit()



            message="Bill Generated : "+bill+" Total ₹"+str(total)






    # available medicines


    cur.execute(

    """

    SELECT * FROM medicines

    WHERE quantity>0

    ORDER BY name

    """

    )


    medicines=cur.fetchall()





    cur.execute(

    """

    SELECT * FROM sales

    ORDER BY id DESC

    """

    )


    sales=cur.fetchall()





    conn.close()





    return render_template_string(

        sales_page,

        medicines=medicines,

        sales=sales,

        message=message

    )





# ================= PART 4 END =================
# =====================================================
# PART 5
# REPORTS + BACKUP + FINAL RUN
# =====================================================



# ================= REPORT PAGE =================



report_page = """

<!DOCTYPE html>

<html>


<head>


<title>
Reports
</title>



<style>


body{

font-family:Arial;

background:#f1f5f4;

}



.box{

background:white;

margin:30px;

padding:30px;

border-radius:15px;

box-shadow:0 0 10px #ccc;

}



.card{

display:inline-block;

background:#009879;

color:white;

padding:25px;

margin:10px;

width:180px;

text-align:center;

border-radius:10px;

}



table{

width:100%;

border-collapse:collapse;

margin-top:20px;

}



th{

background:#009879;

color:white;

}



td,th{

padding:10px;

border:1px solid #ddd;

text-align:center;

}



.alert{

color:red;

font-weight:bold;

}



a{

color:#009879;

text-decoration:none;

}



</style>


</head>



<body>



<div class="box">



<a href="/dashboard">

← Dashboard

</a>




<h2>
Pharmacy Reports
</h2>





<div class="card">

<h1>
{{medicine_count}}
</h1>

Medicines

</div>





<div class="card">

<h1>
₹{{sales_total}}
</h1>

Sales

</div>





<div class="card">

<h1>
₹{{purchase_total}}
</h1>

Purchase

</div>






<h2>
Low Stock Alert
</h2>



<table>


<tr>

<th>
Medicine
</th>


<th>
Quantity
</th>


</tr>




{% for m in low_stock %}



<tr>


<td>
{{m[1]}}
</td>


<td class="alert">

{{m[6]}}

</td>



</tr>



{% endfor %}



</table>







<h2>
Expired Medicines
</h2>




<table>


<tr>

<th>
Medicine
</th>


<th>
Expiry
</th>


</tr>




{% for e in expired %}




<tr>


<td>
{{e[1]}}
</td>


<td class="alert">

{{e[7]}}

</td>


</tr>




{% endfor %}



</table>






</div>



</body>


</html>


"""







@app.route("/reports")

def reports():


    if "user" not in session:

        return redirect("/")



    conn=db()

    cur=conn.cursor()




    cur.execute(

    "SELECT COUNT(*) FROM medicines"

    )


    medicine_count=cur.fetchone()[0]






    cur.execute(

    "SELECT SUM(total) FROM sales"

    )


    sales_total=cur.fetchone()[0]


    if sales_total is None:

        sales_total=0





    cur.execute(

    "SELECT SUM(quantity*price) FROM purchases"

    )


    purchase_total=cur.fetchone()[0]


    if purchase_total is None:

        purchase_total=0







    cur.execute(

    """

    SELECT * FROM medicines

    WHERE quantity < 10

    """

    )


    low_stock=cur.fetchall()





    today=datetime.now().strftime("%Y-%m-%d")



    cur.execute(

    """

    SELECT * FROM medicines

    WHERE expiry < ?

    """,

    (today,)

    )



    expired=cur.fetchall()



    conn.close()






    return render_template_string(

        report_page,

        medicine_count=medicine_count,

        sales_total=sales_total,

        purchase_total=purchase_total,

        low_stock=low_stock,

        expired=expired

    )






# ================= BACKUP =================



@app.route("/backup")

def backup():


    if "user" not in session:

        return redirect("/")



    if os.path.exists(DATABASE):


        shutil.copy(

            DATABASE,

            "pharmacy_backup.db"

        )


        msg="Backup Created Successfully"


    else:


        msg="Database Not Found"





    return """

    <html>

    <body style="font-family:Arial;text-align:center;margin-top:100px">


    <h1>

    Database Backup

    </h1>


    <h3>

    """+msg+"""

    </h3>



    <a href="/dashboard">

    Back Dashboard

    </a>


    </body>


    </html>

    """







# =====================================================
# SHOW ALL ROUTES
# =====================================================


print("\nAVAILABLE ROUTES")

for r in app.url_map.iter_rules():

    print(r)





# =====================================================
# START APPLICATION
# =====================================================



if __name__=="__main__":


    app.run(

        debug=True

    )
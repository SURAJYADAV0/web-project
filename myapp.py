from flask import Flask, render_template, request, redirect, session
import pymysql as p

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key for sessions

def getconnect():
    return p.connect(host="localhost", port=3307, user="root", password="newpassword", database="suraj")

def getdata():
    db = getconnect()
    cr = db.cursor()
    sql = "select name, password from student"
    cr.execute(sql)
    data = cr.fetchall()
    db.commit()
    db.close()
    return data

def insertrec(t):
    db = getconnect()
    cr = db.cursor()
    sql = "insert into student values(%s,%s,%s,%s,%s)"
    cr.execute(sql, t)
    db.commit()
    db.close()

def getalldata():
    db = getconnect()
    cr = db.cursor()
    sql = "select * from student"
    cr.execute(sql)
    data = cr.fetchall()
    db.commit()
    db.close()
    return data

def getdatabyid(ids):
    db = getconnect()
    cr = db.cursor()
    sql = "select * from student where id=%s"
    cr.execute(sql, ids)
    data = cr.fetchone()
    db.commit()
    db.close()
    return data

def updatedata(t):
    db = getconnect()
    cr = db.cursor()
    sql = "update student set name=%s,email=%s,address=%s,password=%s where id=%s"
    cr.execute(sql, t)
    db.commit()
    db.close()

def deletedata(ids):
    db = getconnect()
    sql = 'delete from student where id=%s'
    cr = db.cursor()
    cr.execute(sql, ids)
    db.commit()
    db.close()

#==========================flask================================
@app.route('/')
def login():
    return render_template("page1.html")

@app.route("/registration")
def register():
    return render_template("page2.html")

@app.route("/validateuser", methods=["POST"])
def valid_user():
    usern = request.form["uname"]
    pasw = request.form["pin"]
    data = (usern, pasw)
    database = getdata()
    if data in database:
        return render_template('home.html')
    else:
        return render_template("page2.html")

@app.route("/insertrec", methods=["POST"])
def signup():
    ids = request.form['id']
    uname = request.form['uname']
    email = request.form['email']
    address = request.form['address']
    passw = request.form['pin']
    t = (ids, uname, email, address, passw)
    insertrec(t)
    return redirect("/registration")

@app.route("/user")
def user_list():
    if 'admin' not in session:
        return redirect('/adminlogin')
    userlist = getalldata()
    return render_template("user.html", ulist=userlist)

@app.route("/updateuser/<int:ids>")
def update_user(ids):
    if 'admin' not in session:
        return redirect('/adminlogin')
    d = getdatabyid(ids)
    return render_template("edituser.html", data=d)

@app.route("/updaterec", methods=["POST"])
def update_rec():
    if 'admin' not in session:
        return redirect('/adminlogin')
    ids = request.form["id"]
    uname = request.form["uname"]
    email = request.form["email"]
    add = request.form["address"]
    passw = request.form["pin"]
    t = (uname, email, add, passw, ids)
    updatedata(t)
    return redirect("/user")

@app.route("/deleteuser/<int:ids>")
def delete_user(ids):
    if 'admin' not in session:
        return redirect('/adminlogin')
    deletedata(ids)
    return redirect("/user")

@app.route("/adminlogin")
def admin_login():
    return render_template('admin_login.html')

@app.route("/adminvalidate", methods=['POST'])
def admin_validate():
    admin_user = request.form['admin_user']
    admin_pass = request.form['admin_pass']
    
    # Hardcoded admin credentials for demonstration
    if admin_user == 'suraj'and admin_pass == 'suraj45':
        session['admin'] = True
        return redirect('/user')  # Redirect to user list or admin dashboard
    else:
        return "Only Admin Can Login", 403

@app.route("/adminlogout")
def admin_logout():
    session.pop('admin', None)
    return redirect('/')

@app.route("/mobiles")
def m():
    return render_template("mobile.html")

@app.route("/laptops")
def l():
    return render_template("laptop.html")

@app.route("/Clothing")
def c():
    return render_template("Clothing.html")

@app.route("/tv")
def t():
    return render_template("tv.html")

if __name__ == "__main__":
    app.run(debug=True)

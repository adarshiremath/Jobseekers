from flask import Flask, redirect, url_for, request, render_template, redirect, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jobseekers'

mysql = MySQL(app)



@app.route("/")
def home():
    return render_template("index.html") 

@app.route('/jobseeker/login', methods=['GET','POST'])
def login_js():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        cur = mysql.connection.cursor()
        user = cur.execute("SELECT * from jobseeker WHERE email = (%s)", [email])
        userdetails = cur.fetchall()
        print(userdetails)
        if user > 0:
            passwd = userdetails[0][5]
            print(passwd)
            if password == passwd:
                id1 = userdetails[0][0]
                print(id1)
                return redirect(url_for('db_js', id = id1))
            return render_template("signinjs.html")
    return render_template("signinjs.html")    

    
@app.route('/jobseeker/register', methods=['GET','POST'])
def register_js():
    if request.method == 'POST':
        name = (str(request.form.get('fname'))+ str(" ") + str(request.form.get('lname')))
        email = request.form.get('jsemail')
        password = request.form.get('jspwd')
        gender = request.form.get('gender')
        phno = request.form.get('jsphone')
        experience = request.form.get('jsexperience')
        projects = request.form.get('jsprojects')
        internships = request.form.get('jsinternships')
        skills = request.form.get('jsskills')
        img = request.files['imgfile']
        resume = request.files['resumefile']
           

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO jobseeker (name1, email, sex, phone, passwd1) VALUES (%s,%s,%s,%s,%s)", (name, email, gender, phno, password))
        cur.execute("SELECT seekerid from jobseeker where email = (%s)", [email])
        s_id = cur.fetchone()
        cur.execute("INSERT INTO portfolio (seekerid, experience, projects, internships, skills) VALUES (%s,%s,%s,%s,%s)", (int(s_id[0]), experience, projects, internships, skills))
        # cur.execute("INSTER INTO js_docs (seekerid,pic, resum) VALUES (%s,%s,%s)", (int(s_id[0]), imgbinarydata, resbinarydata))
        mysql.connection.commit()
        cur.close()
        return "<script>window.onload = window.close();</script>"
    return render_template("registerjs.html")

@app.route("/employer/login", methods=['GET','POST'])
def login_emp():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        cur = mysql.connection.cursor()
        user = cur.execute("SELECT * from employer WHERE email = (%s)", [email])
        userdetails = cur.fetchall()
        if user > 0:
            passwd = userdetails[0][5]
            if password == passwd:
                id1 = userdetails[0][0]
                return redirect(url_for('db_emp', id = id1))
            return render_template("signinemp.html")
    return render_template("signinemp.html")  


@app.route("/employer/register", methods=['GET','POST'])
def register_emp():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('eemail')
        password = request.form.get('epwd')
        phno = request.form.get('ephone')
        location = request.form.get('location')
        img = request.files['imgfile']
        
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employer (name2, email, location, phone, passwd2) VALUES (%s,%s,%s,%s,%s)", (name, email, location, phno, password))
        cur.execute("SELECT compid from employer where email = (%s)", [email])
        e_id = cur.fetchone()
        # cur.execute("INSTER INTO js_docs (compid, pic) VALUES (%s,%s)", (int(e_id[0]), str(img.read())))
        mysql.connection.commit()
        cur.close()
        return "<script>window.onload = window.close();</script>"
    return render_template("registeremp.html") 



@app.route("/jobseeker/<id>/dashboard")
def db_js(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from jobseeker WHERE seekerid = (%s)", [id])
    userdetails1 = cur.fetchone()
    cur.execute("SELECT * from portfolio WHERE seekerid = (%s)", [id])
    userdetails2 = cur.fetchone()
    return render_template('jobseeker_dashboard.html', user1 = userdetails1, user2 = userdetails2)

@app.route("/employer/<id>/dashboard")
def db_emp(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from employer WHERE compid = (%s)", [id])
    userdetails = cur.fetchone()
    return render_template("employer_dashboard.html", user = userdetails)

@app.route("/jobseeker/find", methods=['GET','POST'])
def search_js():
    if request.method == 'POST':
        location = request.form.get('location')
        company = request.form.get('company')
        role = request.form.get('role')
        salmax = request.form.get('salmax')
        salmin = request.form.get('salmin')
        print(location, company, role, salmax, salmin)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from jobs") #WHERE title LIKE %(%s)%", (role))
        userdetails1 = cur.fetchall()
        cur.execute("SELECT * from dept WHERE location = (%s)", [location])
        userdetails2 = cur.fetchall()
        return render_template("jobseeker_searchpage.html", user1 = userdetails1, length = len(userdetails2), user2 = userdetails2)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from jobs")
    userdetails1 = cur.fetchall()
    cur.execute("SELECT * from dept")
    userdetails2 = cur.fetchall()
    return render_template("jobseeker_searchpage.html", user1 = userdetails1, length = len(userdetails1), user2 = userdetails2)

@app.route("/jobseeker/find/<id>")
def job_desc(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from jobs WHERE jobid =  (%s)",[id])
    userdetails1 = cur.fetchone()
    cur.execute("SELECT * from dept WHERE jobid =  (%s)",[id])
    userdetails2 = cur.fetchone()
    return render_template("jobdesc.html", user1 = userdetails1, user2 = userdetails2)    

@app.route("/employer/find")
def search_emp():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from jobseeker")
    userdetails1 = cur.fetchall()
    cur.execute("SELECT * from portfolio")
    userdetails2 = cur.fetchall()
    return render_template("emp_search_js.html", user1 = userdetails1, length = len(userdetails1), user2 = userdetails2)

@app.route("/employer/addjobs", methods=['GET','POST'])
def jobs():
    if request.method == 'POST':
        company = request.form.get('Company')
        title = request.form.get('title')
        dept = request.form.get('dept')
        location = request.form.get('location')
        salary = request.form.get('salary')
        Eligibility = request.form.get('Eligibility')
        desc = request.form.get('desc')
        print(company, title, location, salary, desc)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO jobs (company, title, salary, eligibility, descp) VALUES (%s,%s,%s,%s,%s)", (company, title, salary, Eligibility, desc))
        cur.execute("SELECT jobid from jobs where title = (%s)", [title])
        j_id = cur.fetchone()
        cur.execute("INSERT INTO dept (jobid, dname, location) VALUES (%s,%s,%s)", (int(j_id[0]), dept, location))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('db_emp'))
    return render_template("postjob.html")   

@app.route("/jobseeker/saved_jobs", methods=['GET','POST'])
def saved_jobs():
    return render_template("jobseeker_savedjobs.html")

@app.route("/employer/saved_applications", methods=['GET','POST'])
def saved_applications():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from jobseeker")
    userdetails1 = cur.fetchall()
    cur.execute("SELECT * from portfolio")
    userdetails2 = cur.fetchall()
    return render_template("emp_saved_application.html", user1 = userdetails1, length = len(userdetails1), user2 = userdetails2)   

# @app.route("/under_construction")
# def under_construction():
#     return render_template("emp_saved_application.html")


if __name__ == "__main__":
    app.run(debug= True)

    
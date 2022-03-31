from flask import Flask, request, g, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import pandas as pd
from database import DB
from datetime import timedelta

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.sqlite3'
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/webapp/userInfo'
app.secret_key = 'bbbbbbbbbbbbbb'
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)
querySel = DB()

db.Model.metadata.reflect(db.engine)

# create dataset for user accounts
class login(db.Model):
    __table_args__ = {'extend_existing': True}
    _id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    uname = db.Column(db.String(100))
    password = db.Column(db.String(256))
    def __init__(self, fname, lname, email, uname, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.uname = uname
        self.password = password

# user login page
@app.route('/', methods = ['POST','GET'])
def startingPage():
    if(request.method == 'POST'):
        userName = request.form.get('username')
        password = str(request.form.get('password'))
        encPass = hashlib.sha256(password.encode()).hexdigest()
        valid = login.query.filter_by(uname=userName, password=encPass).first()
        if valid:
            session['uname'] = valid.uname
            session['fname'] = valid.fname
            session['lname'] = valid.lname
            session['email'] = valid.email
            return redirect("/dashboard")
        else:
            flash('Login failed')

    return render_template("login.html")

# user create account page
@app.route('/createAccount', methods = ['POST', 'GET'])
def createAccountPage():
    if(request.method == 'POST'):
        session.permanent = True
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        email = request.form.get('email')
        userName = request.form.get('username')
        password = str(request.form.get('password'))
        encPass = hashlib.sha256(password.encode()).hexdigest()
        newUser = login(firstName, lastName, email, userName, encPass)

        db.session.add(newUser)
        db.session.commit()
        return redirect("/")

    return render_template("createaccount.html")

# display the Kroger customers' info and transaction database

@app.route('/dashboard', methods = ['POST', 'GET'])
def displayDashboard():
	if(request.method == 'POST'):
		return
	return render_template("dashboard.html")

@app.route('/dashboardResults', methods = ['POST', 'GET'])
def displayDashboardResults():
    if(request.method == 'POST'):
        hshdNum = int(request.form['hshdNum'])

        hshdData = querySel.getHouseHoldData(int(hshdNum))

        request_data = {
        'hshdNum': hshdNum,
        'houseData': hshdData
        }
    return render_template("dashboardResults.html", **request_data)

@app.route('/answer1')
def getAnswer1():
    total = querySel.getTotalSales()

    for num in total:
        num[1] = round(num[1], 2)

    request_data = {
        'total': total,
        }
    return render_template("answer1.html", **request_data)

@app.route('/answer2')
def getAnswer2():
    total1 = querySel.getTotalSalesChildFew()
    total2 = querySel.getTotalSalesChildMany()
    count1 = querySel.getCountChildFew()
    count2 = querySel.getCountSalesChildMany()
    

    for num in total1:
        num[1] = round(num[1], 2)

    for num in total2:
        num[1] = round(num[1], 2)

    request_data = {
        'total1': total1,
        'total2': total2,
        'count1': count1,
        'count2': count2
        }
    return render_template("answer2.html", **request_data)

#allow users upload database
@app.route('/uploadCSV')
def uploadCSV():
    return render_template("upload.html")

#DATA PULL for user uploaded files
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    ans = 1
    if request.method == 'POST':
        #open('templates/upload_results.html', 'w').close()
        # get inputs from previous page
        fHouseholds = request.files['file1']
        fProducts = request.files['file2']
        fTransactions = request.files['file3']
        year = int(request.form.get('year_2'))
        hshd_num = int(request.form.get('hshd_num_2'))

        # read dataframe 
        dfHouseholds = pd.read_csv(fHouseholds)
        dfProducts = pd.read_csv(fProducts)
        dfTransactions = pd.read_csv(fTransactions)

        # remove space from columns' names
        dfHouseholds.columns = dfHouseholds.columns.str.replace(' ', '')
        dfProducts.columns = dfProducts.columns.str.replace(' ', '')
        dfTransactions.columns = dfTransactions.columns.str.replace(' ', '')

        # DATA PULLS
        new_df = dfTransactions.loc[(dfTransactions['HSHD_NUM'] == hshd_num) & (dfTransactions['YEAR'] == year)]
        mergerHSHDWithTRANS = pd.merge(new_df, dfHouseholds,   how = "left", on = 'HSHD_NUM')
        mergeWithPROD = pd.merge(mergerHSHDWithTRANS, dfProducts,   how = "left", on = 'PRODUCT_NUM')
        mergeWithPROD = mergeWithPROD.drop_duplicates()
        removeCOL = mergeWithPROD[['HSHD_NUM','PURCHASE_','BASKET_NUM','COMMODITY','PRODUCT_NUM','DEPARTMENT']]
        ans =removeCOL
        
        # Convert to html before rendering
        #html = removeCOL.to_html()
        #text_file = open("templates/upload_results.html", "w")
        #text_file.write('<form action="/uploadCSV" method="GET"><div class="flex-container"><div class="flex-item"><button id="getA" type="submit">Go to Upload Page</button></div></div></form>')
        #text_file.write(html)
        #text_file.close()
    return render_template("upload_results.html", tables =[ans.to_html()], titles=ans.columns.values)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
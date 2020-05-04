#imports
from flask import Flask,render_template,request,redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime,date,timedelta
import sqlite3
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
from flask_datepicker import datepicker

##############################################


app = Flask(__name__)
Bootstrap(app)
db=SQLAlchemy(app)
admin =Admin(app)
datepicker(app)
# datepicker.loader(theme="base")

app.config['SECRET_KEY'] = '123456'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
conn = sqlite3.connect('test.db')

##############  Database ###############3

class Patient(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50))
    phone= db.Column(db.String(50))
    date_created= db.Column(db.Date,default=date.today())
    area= db.Column(db.String(30))
    age=db.Column(db.Integer)
    sex= db.Column(db.String(8))
    treatments=db.relationship('Treatment',backref='owner')

    def __repr__(self):

       return f"Patient('{self.id}','{self.name}','{self.phone}','{self.date_created}','{self.area}','{self.age}','{self.sex}')"




class Treatment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=True)
    complaint=db.Column(db.String())
    treatment=db.Column(db.String())
    report=db.Column(db.String())
    fee=db.Column(db.Integer())
    date_treatment= db.Column(db.Date,default=date.today())
    date_nextappointment= db.Column(db.Date())

    def __repr__(self):
        return f"Treatment['{self.id}','{self.patient_id}','{self.complaint}','{self.treatment}','{self.date_treatment}','{self.date_nextappointment}']"

def patient_query():
    return Patient.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=patient_query,allow_blank=False)


###### Flask Routes #####
@app.route('/',methods=['GET', 'POST'])
def redirected():
    ab= date.today()
    xy=ab.strftime("%m/%d/%Y")

    # todayappointment=Treatment.query.filter_by(Treatment.date_nextappointment=datetime.now).all()
    # print(todayappointment)
    one_weeks_ago = ab - timedelta(weeks=1)
    all1=Treatment.query.filter_by().all()
    all2=Treatment.query.filter(one_weeks_ago>Treatment.date_treatment).all()
    starting_today=0
    starting=0
    starting2=0

    for y in range(len(all2)):
        starting2=starting2+all2[y].fee



    for x in range(len(all1)):
        
        # print(all1[x].fee)
        starting=starting+all1[x].fee
        if(all1[x].date_nextappointment==xy):
            starting_today=starting_today+1
           

    

    return render_template('dashbord.html',xy=xy,starting=starting,starting_today=starting_today,starting2=starting2)



@app.route('/consulting',methods=['GET', 'POST'])
def consulting():
    form = ChoiceForm()


   
    if request.method == 'POST':
        req1=request.form
        opts=req1.get('opts')
        complaint=req1.get('complaint')
        treatment=req1.get('treatment') 
        report=req1.get('report')
        date_nextappointment1=req1.get('date_nextappointment')
        fee=req1.get('fee')
        date_nextappointment=datetime.strptime(date_nextappointment1,"%Y-%m-%d")
        newtreatment= Treatment(patient_id=opts,complaint=complaint,treatment=treatment,report=report,fee=fee,date_nextappointment=date_nextappointment)
        db.session.add(newtreatment)
        db.session.commit()
        # print(newtreatment)
        # print(opts)
    return render_template('consulting.html',form=form)



@app.route('/newpatient',methods=['GET', 'POST'])
def newpatient():
    if request.method=='POST':
        req=request.form
        name=req.get('name')
        phone=req.get('phone')
        area=req.get('area')
        age=req.get('age')
        sex=req.get('sex')
        newpatient = Patient(name=name,phone=phone,area=area,age=age,sex=sex)
        db.session.add(newpatient)
        db.session.commit()
        # print(name,phone,area,age,sex)
        return redirect('/consulting')
    return render_template('newpatient.html')

@app.route('/viewall',methods=['GET', 'POST'])
def patient():
    c=0
    form = ChoiceForm()
    oldnew=Patient.query.filter_by(id=1).first()
    increment=0
    if request.method == 'POST':
        
        req123=request.form
        opts=req123.get('opts')

        
        oldnew=Patient.query.filter_by(id=opts).first()
        mynew=Treatment.query.filter_by(patient_id=opts).all()
        for mynews in mynew:
            
            c +=mynews.fee
        return render_template('viewall.html',form=form,mynew=mynew,oldnew=oldnew,c=c)
        
    return render_template('viewall.html',form=form,oldnew=oldnew,increment=increment)

@app.route("/editdata")
def editdata():
    return redirect('/admin')
    
@app.route("/upcomming",methods=["GET", "POST"])
def upcomming():
    xyz = date.today()
    list=[]
    list1=[]
    # name1=[]
    if request.method == 'POST':
        reqdate = request.form
        scheduledate=reqdate.get('scheduledate')
        name=Treatment.query.filter(Treatment.date_nextappointment==scheduledate).all()
        for l in range(len(name)):
            a=name[l].patient_id
            list.append(a)
        
        for lists in list:
            cool=Patient.query.filter(Patient.id==lists).first()
            list1.append(cool)


        

        
    return render_template('upcomming.html',list1=list1)



###### Admin #######
admin.add_view(ModelView(Patient,db.session))
admin.add_view(ModelView(Treatment,db.session))

if __name__ == '__main__':
    app.run(debug=True)
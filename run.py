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
##############################################


app = Flask(__name__)
Bootstrap(app)
db=SQLAlchemy(app)
admin =Admin(app)


app.config['SECRET_KEY'] = '123456'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config['WHOOSH_BASE']='whoosh'
conn = sqlite3.connect('test.db')
# wa.whoosh_index=(app,Patient)

##############  Database ###############3

class Patient(db.Model):
    # __searchable__=['name', 'phone']
    id =db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50))
    phone= db.Column(db.String(50))
    date_created= db.Column(db.Date,default=date.today())
    area= db.Column(db.String(30))
    age=db.Column(db.Integer)
    sex= db.Column(db.String(8))
    treatments=db.relationship('Treatment',backref='owner')

    def __repr__(self):

       return f"{self.name},{self.phone},{self.id},{self.date_created},{self.area},{self.age},{self.sex}"




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
        return f"Treatment['{self.id}',{self.patient_id},'{self.complaint}','{self.fee}','{self.treatment}','{self.date_treatment}','{self.date_nextappointment}']"

def patient_query():
    return Patient.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=patient_query,allow_blank=False)




@app.route('/temp',methods=['GET', 'POST'])
def temp():
    all1=Patient.query.filter_by().all()
    
    if request.method == 'POST':
        req1=request.form
        opts=req1.get('patient')
       
        li = list(opts.split(",")) 
        print(li)
        f=li[2]
        print(f)
    return render_template('temp.html',all1=all1)







###### Flask Routes #####
@app.route('/',methods=['GET', 'POST'])
def redirected():
    ab= date.today()
    xy=ab.strftime("%m/%d/%Y")
    a=0

    total=Treatment.query.filter(Treatment.date_nextappointment==ab)

    for totals in total:
        a=a+1

    

    return render_template('dashbord.html',xy=xy,a=a)



@app.route('/consulting',methods=['GET', 'POST'])
def consulting():
    form = ChoiceForm()
    all1=Patient.query.filter_by().all()


   
    if request.method == 'POST':
        req1=request.form
        opts=req1.get('patient') 
        li = list(opts.split(",")) 
        print(li)
        f=li[2]
        
        complaint=req1.get('complaint')
        treatment=req1.get('treatment') 
        report=req1.get('report')
        date_nextappointment1=req1.get('date_nextappointment')
        fee=req1.get('fee')
        date_nextappointment=datetime.strptime(date_nextappointment1,"%Y-%m-%d")
        newtreatment= Treatment(patient_id=f,complaint=complaint,treatment=treatment,report=report,fee=fee,date_nextappointment=date_nextappointment)
        db.session.add(newtreatment)
        db.session.commit()
        # print(newtreatment)
        print(opts)
    return render_template('consulting.html',form=form,all1=all1)



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

@app.route('/history',methods=['GET', 'POST'])
def patient():
    c=0
    all1=Patient.query.filter_by().all()

    oldnew=Patient.query.filter_by(id=1).first()
    increment=0
    if request.method == 'POST':
        
        req123=request.form
        opts=req123.get('patient') 
        li = list(opts.split(",")) 
        print(li)
        f=li[2]

        
        oldnew=Patient.query.filter_by(id=f).first()
        mynew=Treatment.query.filter_by(patient_id=f).all()
        for mynews in mynew:
            
            c +=mynews.fee
        return render_template('history.html',mynew=mynew,oldnew=oldnew,c=c,all1=all1)
        
    return render_template('history.html',oldnew=oldnew,increment=increment,all1=all1)


    
@app.route("/appointment",methods=["GET", "POST"])
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


        

        
    return render_template('appointment.html',list1=list1)

@app.route('/viewday',methods=['GET', 'POST'])
def viewday():
    xyz = date.today()
    scheduledate=xyz
    total=0
    list1=[]
    
    if request.method == 'POST':
        reqdate = request.form
        scheduledate=reqdate.get('scheduledate')
        name=Treatment.query.filter(Treatment.date_treatment==scheduledate).all()
        for names in name:
            total=total+names.fee
            
            list1.append(names)

    return render_template('viewday.html',list1=list1,scheduledate=scheduledate,total=total)
            
    return render_template('viewday.html',list1=list1,scheduledate=scheduledate,total=total)


@app.route('/weekly',methods=['GET', 'POST'])
def weekly():
    xyz = date.today()
    week= xyz - timedelta(weeks=1)
    month=xyz - timedelta(weeks=31)
    year=xyz - timedelta(days=365)
    report = week
    scheduledate=xyz
    total=0
    list1=[]
    report=week
    if request.method == 'POST':
        req=request.form
        report=req.get('report')
        print(report)
   
    
        name=Treatment.query.filter(Treatment.date_treatment>=report).all()
        for names in name:
            total=total+names.fee
        
            list1.append(names)


    return render_template('weekly.html',list1=list1,scheduledate=scheduledate,total=total,week=week,month=month,year=year,report=report)
            
    return render_template('weekly.html',list1=list1,scheduledate=scheduledate,total=total,week=week,month=month,year=year,report=report)


@app.route("/editdata")
def editdata():
    return redirect('/admin')
###### Admin #######
admin.add_view(ModelView(Patient,db.session))
admin.add_view(ModelView(Treatment,db.session))

if __name__ == '__main__':
    app.run(debug=True)
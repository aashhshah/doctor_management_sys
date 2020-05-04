from run import db,Treatment,Patient
from datetime import datetime,date,timedelta

xyz = date.today()
name=Treatment.query.filter(Treatment.date_nextappointment==xyz).all()
list=[]


for l in range(len(name)):
    
    a=name[l].patient_id
    #print(a)
    list.append(a)

for lists in list:
    # print(lists)
    cool=Patient.query.filter(Patient.id==lists).first()
    print(cool)    

from run import db,Treatment,Patient
from datetime import datetime,date,timedelta
xy = date.today()

xyz = date.today()
name=Treatment.query.filter(Treatment.date_nextappointment==xyz).all()


for x in range(len(name)):
    
    c=name[x].patient_id
    for 
    
     in c:

        name1=Patient.query.filter(Patient.id==c).all()
        print(name1)
    

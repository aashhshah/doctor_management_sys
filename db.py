from run import db,Treatment,Patient
from datetime import datetime,date,timedelta

xyz = date.today()
list=[]
list1=[]


# a=Patient.query.filter(Patient.id==names.patient_id).first()
# a=Patient.query.filter().all()
day=xyz- timedelta(days=1)
day2=xyz - timedelta(days=2)
week= xyz - timedelta(weeks=1)
month=xyz - timedelta(weeks=31)
year=xyz - timedelta(days=365)

name=Treatment.query.filter(Treatment.date_treatment>day2).all()

print(Treatment.id)
print(day2)



# # print(name)
# for l in range(len(name)):
    
#     a=name[l].id
#     #print(a)
#     list.append(a)
# print(list)
# # for lists in list:
# #     # print(lists)
# #     cool=Patient.query.filter(Patient.id==lists).first()
# #     print(cool)
     

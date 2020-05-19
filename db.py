from run import db,Treatment,Patient
from datetime import datetime,date,timedelta

xyz = date.today()
list=[]

name=Treatment.query.filter(Treatment.date_nextappointment==xyz).all()
for names in name:
    a=Patient.query.filter(Patient.id==names.patient_id).first()
    # print(names)
    # print(a)
    thisdict={"name":a.name,"fee":names.fee,"treatment":names.treatment}
    # print(thisdict.get("treatment"))
    list.append(thisdict)


for lists in list:
    print(thisdict["name"])









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
     

from run import db,Treatment,Patient
from datetime import datetime,date,timedelta
xy = date.today()

all1=Treatment.query.filter_by().all()
# print(all1[11])
one_weeks_ago = xy - timedelta(weeks=1)

all2=Treatment.query.filter(Treatment.date_treatment>one_weeks_ago).all()

starting2=0



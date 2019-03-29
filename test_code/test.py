# counts=['a','b','c','a']
# a = list()
# [a.append(i) for i in counts if a.count(i)==0]
# print(a)
import datetime
import time
def get_current_week_begin_timestamp():
    date1 = datetime.datetime.now()
    print(date1)
    this_week_start_dt = str(date1 - datetime.timedelta(days=date1.weekday())).split()[0]
    print(this_week_start_dt)
    timestamp = int(time.mktime(datetime.datetime.strptime(this_week_start_dt, "%Y-%m-%d").timetuple()))
    print(timestamp)

get_current_week_begin_timestamp()
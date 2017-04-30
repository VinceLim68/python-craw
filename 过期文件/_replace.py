import datetime
a = "2012-05-01 23:59:59.0"
a = a.replace('.0','')
# print type(datetime.date.today())
b = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S").date()
print type(b)
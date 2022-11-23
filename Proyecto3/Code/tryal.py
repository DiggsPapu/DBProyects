import datetime
from PersonTypes.AdminCreateRole import AdminCreateRole
from PersonTypes.Instructor import Instructor
from PersonTypes.User import User
from Connection.ConectDB import *
# valores = getUser("iol","iol")
# print(valores)
# ins2 = Instructor(valores)
# ins2.getInstructorContract()
# values= ["raulalbiol","RaulAlbiol","Raul Albiol","Raul av","Instructor"]
# ins = Instructor(values)
# ins.cursor.execute('''select * from sesion where current_date<sesiondate and workerid = '{}' '''.format(ins.worker_id))
# val = ins.cursor.fetchall()
# print(val)
x = datetime.datetime(2022,11,24,2)
y = datetime.time(0,59,0)
print(y.__str__())
print(x)
print(x.date())
print(x.time())
print(x.now())
print(x.now()<x)
# ins.cursor.execute('''delete from excategory where excategory.category = '{}' '''.format("Weight"))
# ins.cursor.execute('''insert into sesion(sesionname,sesiondate,sesionhour,sesionstatus,description,workerid,categorycode)
#         values('{}','{}','{}','WAIT','{}','{}',{})'''
#         .format("Zuper zumba",str(x.date()),str(x.time()),input("Enter the description of the sesion: "),ins.worker_id,str(1)) )
# ins.cursor.execute('''select * from sesion where workerid = '{}' '''.format(ins.worker_id))
# values = ins.cursor.fetchall()
# for x in values:
#             print(x)
#             print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))

# ins.cursor.execute('''delete from sesion where sesioncode = {} '''.format("1"))
values = ["postgres","Manager123","Diego Alonzo","Raul av","Superuser"]
inst = AdminCreateRole(values)
inst.createAdminReportery("reportery1","reportery1","Juan Carlos","San cris")
# inst.createUser("dieggspapu","Manager123","Diego Alonzo","2002-01-20","1.8","80","1 av","32","DIAMOND","DEBIT","1234123412341234")
# values = ["dieggspapu","Manager123","Diego Alonzo","2002-01-20","1.8","80","1 av"]
# user = User(values)
# user.endSubscription(inst.cursor)
# user.saveUser()
# user.showThisWeek()
# user.searchSesionByInstructor()
# date_val = user.enterDate()
# user.cursor.execute('''select * from sesion where sesiondate = '{}' '''.format(date_val.date()))
# values = user.cursor.fetchall()
# count = 1
# for x in values:
#     print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))
#     count+=1
# sesioncode = user.enterInteger()
# while (sesioncode<1 or sesioncode>count):
#     sesioncode = user.enterInteger()
# user.cursor.execute('''insert into sesionuser (userid,sesioncode)
# values('{}',{})'''.format(user.userid,str(values[sesioncode-1][0])))
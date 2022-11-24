import datetime
import names 
from PersonTypes.AdminCreateRole import *
from PersonTypes.Instructor import *
from PersonTypes.User import *
from Connection.ConectDB import *
# valores = getUser("iol","iol")
# print(valores)
# ins2 = Instructor(valores)
# ins2.getInstructorContract()
values= ["raulalbiol","RaulAlbiol","Raul Albiol","Raul av","Instructor"]
ins = Instructor(values)

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
print(datetime.date(2022,1,1).today().__str__())
def randomBirthdate():
    start_date = datetime.date(1940, 1, 1)
    end_date = datetime.date(2013, 1, 1)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.__str__()
print(randomBirthdate())
def randomDate(cursor):
    cursor.execute('''select current_date+interval'6 month' ''')
    end_date = cursor.fetchone()[0]
    cursor.execute('''select current_date+interval'1 day' ''')
    start_date = cursor.fetchone()[0]
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.__str__()
print(randomDate(connect()))
def randomDateHourTomorrow(cursor):
    cursor.execute('''select current_date+interval'1 day' ''')
    return [cursor.fetchone()[0].date().__str__(),datetime.time(random.randint(5,22),0,0).__str__(),datetime.time(0,random.randint(30,59),0).__str__()]
print(randomDateHourTomorrow(connect()))
a = [1,2,3,4,5]
print(random.choice(a))
def simulateOperations():
    cursor = connect()
    cursor.execute('''select current_date ''')
    current_date = cursor.fetchone()[0]
    cursor.execute('''select current_date + interval'6 month' ''')
    proxdate = cursor.fetchone()[0]
    cursor.execute('''select * from usuario''')
    usuarios = cursor.fetchall()
    admin = AdminCreateRole(getUser("postgres","Manager123"))
    for x in range(0,random.randint(0,5)):
        username = name = password = str(names.get_first_name().lower()+str(random.randint(0,2000000)+x))
        subscriptionType=""
        paymentMethod = ""
        if (random.randint(0,1)):
            subscriptionType = "DIAMOND"
        else:
            subscriptionType = 'GOLD'
        if (random.randint(0,1)):
            paymentMethod = "DEBIT"
        else:
            paymentMethod = "CREDIT"
        print('''
        The admin {} created the user {} with the password {}\n'''.format(admin.worker_name,username,password))
        admin.createUser(username,password,name,str(randomBirthdate()),str(1+random.random()),str(random.randint(50,500)),(names.get_full_name()),str(random.randint(12,50)),subscriptionType,paymentMethod,str(1234567890123456)) 
    for x in range (0, random.randint(0,3)):
        username = name = password = str(names.get_first_name().lower()+str(random.randint(0,100)+x+random.randint(0,100)))
        print('''The admin {} created the instructor {} with the password {}'''.format(admin.worker_name,username,password))
        admin.createInstructor(username,password,name,names.get_last_name(),str(random.randint(50,500)),str(1+random.random()))
    cursor.execute('''select * from worker where workertype = 'Instructor' ''')
    instructors = cursor.fetchall()
    for instructor in instructors:
        ins = getUser(instructor[0],instructor[1])
        ins = Instructor(ins)
        ins.cursor.execute('''select current_date''')
        date = ins.cursor.fetchone()[0].__str__()
        print('''
        The instructor {} updated the status of the date {}\n'''.format(ins.worker_id,date))
        ins.updateSesionStatus(date)
        if (random.randint(0,1)):
            category = names.get_last_name()
            print('''
        The instructor {} created a new category named {}\n'''.format(ins.worker_name,category))
            ins.newCategory(category)
        if (random.randint(0,1)):
            ins.worker_name = names.get_last_name()
            ins.worker_direction = names.get_full_name()
            ins.saveInstructor()
            print('''
        The instructor {} updated his profile now he names himself {} and his direction is {}\n'''.format(ins.worker_id,ins.worker_name,ins.worker_direction))
        else:
            pass
        for x in range(0,random.randint(0,5)):
            cursor.execute('''select categorycode from excategory''')
            values = cursor.fetchall()
            time = randomDateHourTomorrow(cursor)
            sesionname = names.get_full_name()
            print('''
        The instructor {} created a new sesion named {}, date {}, hour {}, length {} and type {}'''.format(ins.worker_id,sesionname,time[0],time[1],time[2],str(random.choice(values)[0])))
            ins.createRandomSesion(sesionname,time[0],time[1],time[2],str(random.choice(values)[0]))
            ins.updateSesionStatus(time[0])     
    for usuario in usuarios:
        try:
            user = getUser(usuario[0],usuario[1])
            user = User(user)
            if (random.randint(0,5)==5):
                print('''
        The user {} ended his subscription'''.format(user.userid))
                user.endSubscription(connect())
            for x in range(0,random.randint(0,5)):
                user.assignSesionRandom()
            if (random.randint(0,1)):
                user.direction = names.get_full_name()
                user.name = names.get_first_name()
                user.actualweight = random.randint(50,300)
                user.saveUser() 
                print('''
        The user {} change his profile'''.format(user.userid))
            user.updateSesionValuesRandom()
            cursor.execute('''select userid,avg(caloriesacomplished),avg(heartrate)
            from sesionuser
            inner join sesion
            on sesionuser.sesioncode = sesion.sesioncode
            where sesion.sesiondate = '{}'  and userid = '{}'
            group by userid'''.format('2022-11-25',user.userid))
            values = cursor.fetchone()
            print('''
        The user {} burned {} calories in average and had a heart rate of {}\n'''.format(user.userid,values[1],values[2]))
        except:
            pass
simulateOperations()


# values = ["repo","repo","Repo 1","Repo1","admin_reportery"]
# repo = AdminReportery(values)
# repo.picoHour('2022-11-25')
# repo.simulateOperations(connect())
# values = ["postgres","Manager123","Diego Alonzo","Raul av","Superuser"]
# inst = AdminCreateRole(values)

# inst.createAdminReportery("reportery1","reportery1","Juan Carlos","San cris")
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
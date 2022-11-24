import datetime
from ManagerFunctions import *
def loggedInstructor(username, password, cursor):
    search = '''select * from worker
    inner join(
        select max(contractinstructorcode), workerid, activecontract from instructorcontract
        group by workerid, activecontract
    ) as uc
    on uc.workerid = worker.workerid
    where worker.workerid='''+username+''' and worker.workerpassword =\''''+password+'''\' and uc.activeContract = True'''
    cursor.execute(search)
    instructor = cursor.fetchone()
    if (instructor!=None):
        print("Instructor, "+str(instructor[2])+", welcome to the app.\n\n")  
    else: print("You couldn't logged in, ask administration why.\n")
    return None
def getInstructor(id, cursor):
    cursor.execute('''select * from worker where workerid = {} and workertype = \'Instr\''''.format(id))  
    instructor = cursor.fetchone()
    return instructor   
def configureSesion(workerid, cursor):
    contractcode = str(int(cursor.execute('''select count(sesioncode) from sesion''')[0])+1)
    sesionname = enterSesionName()
    time = checkHour(workerid=workerid, cursor=cursor)
    sesionDate = time[0]
    sesionHour = time[1]
    description = input("Describe what is the sesion about: ")
    categorycode = getCategory(cursor)
    configureSesion = '''insert into excategory(
        sesioncode,sesionname,sesiondate,sesionhour,
        sesionstatus,description,workerid,categorycode
    )
    values(
        '''+contractcode+''',
        \''''+sesionname+'''\',
        \''''+sesionDate+'''\',
        \''''+sesionHour+'''\',
        \'wait\',
        \''''+description+'''\',
        \''''+workerid+'''\'
        '''+categorycode+'''
    )
    '''
    cursor.execute(configureSesion)

def getCategory(cursor):
    while (True):
        cursor.execute('''select category from excategory''')
        values = cursor.fetchall()
        print("These are the categories: ")
        for x in values:
            print(x[0])
        category = input("Enter category: ")
        cursor.execute('''select count(category) from excategory where category = \''''+category+'''\'''')
        if (cursor.fetchone()[0]!=0):
            cursor.execute('''select categorycode from excategory where category = \''''+category+'''\'''')
            return str(cursor.fetchone()[0])
        print("The category does not exist, enter another one.\n")
def enterSesionName():
    while (True):
        name = input("Enter the sesion name, in less than 31 characters: ")
        if (len(name)<=30):
            return name
        print("The entered name exceedes the amount of characters, please try again.\n")
def enterDate():
    while (True):
        birthdate = input("Enter sesion date (YYYY-MM-DD): ")
        birthdateAr = birthdate.split("-")
        try:
            datetime.datetime(int(birthdateAr[0]),int(birthdateAr[1]),int(birthdateAr[2]) )
            if (int(birthdateAr[0])>=2022):
                return birthdate
            print("Your sesion date doesn't make sense, nobody is that old please try again.\n\n")
        except:
            print("Incorrect data format, should be YYYY-MM-DD, please try again.\n\n")
def enterHour():
    while (True):
        hour = input("Enter the hour (HH:MM:SS): ")
        hourAr = hour.split(":")
        try:
            if (0<=int(hourAr[0])<24 and 0<=int(hourAr[1])<60 and 0<=int(hourAr[2])<60):
                return hour
            print("The hour entered is invalid, please try again.\n")
        except:
            print("The hour entered is invalid, please try again.\n")
def checkHour(workerid, cursor):
    while (True):
        date = enterDate()
        hour = enterHour()
        cursor.execute('''select count(sesioncode) from sesion where workerid = '''+str(workerid)+''' and sesiondate = \''''+date+'''\' and sesionhour = \''''+hour+'''\'''')
        if (int(cursor.fetchone()[0])==0):
            facts = [date, hour]
            return facts
        else:
            print("The hour and date entered is already reserved for this instructor.\n")
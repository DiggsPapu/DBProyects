
import datetime
from Connection.ConectDB import connectAdmin
from Objects.UserContract import UserContract

class User:
    def __init__(self,values) -> None:
        self.userid = str(values[0])
        self.password = str(values[1])
        self.name = str(values[2])
        self.birthdate = values[3]
        self.height = str(values[4])
        self.actualweight = str(values[5])
        self.direction = str(values[6])
        self.cursor = connectAdmin(self.userid,self.password)
    def enterDate(self):
        while True:
            try:
                print("Enter the date year.")
                year = self.enterInteger()
                print("Enter the date month.")
                month = self.enterInteger()
                print("Enter the date day.")
                day = self.enterInteger()
                date_value = datetime.datetime(year,month,day)  
                if (date_value > date_value.now()):
                    return date_value
            except:
                pass
            print("The date entered is invalid, please try again")
    
    def searchSesionByDate(self):
        date_val = self.enterDate()
        self.cursor.execute('''select * from sesion where sesiondate = '{}' 
        except all 
        select sesion.sesioncode,sesion.sesionname,sesion.sesiondate,sesion.sesionhour,sesion.timelength,sesion.sesionstatus,sesion.description,sesion.workerid,sesion.categorycode from sesion
        inner join sesionuser 
        on sesionuser.sesioncode = sesion.sesioncode
        where userid = '{}';'''.format(date_val.date(),self.userid))
        values = self.cursor.fetchall()
        codes = []
        if (len(values)!=0):
            print("This are the values: ")
            for x in values:
                print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))
                codes.append(str(x[0]))
            sesioncode = self.enterInteger()
            while (codes.count(str(sesioncode))==0):
                sesioncode = self.enterInteger()
            self.cursor.execute('''insert into sesionuser (userid,sesioncode)
            values('{}',{})'''.format(self.userid,str(sesioncode)))
        else:
            print("There are no available sesions for you at that date ")
    def searchSesionByHour(self):
        print("Enter the hour ")
        hour = self.enterInteger()
        date_val = datetime.time(hour,0,0)
        print(date_val.__str__())
        self.cursor.execute('''select * from sesion where sesionhour = '{}' 
        except all
        select sesion.sesioncode,sesion.sesionname,sesion.sesiondate,sesion.sesionhour,sesion.timelength,sesion.sesionstatus,sesion.description,sesion.workerid,sesion.categorycode from sesion
        inner join sesionuser 
        on sesionuser.sesioncode = sesion.sesioncode
        where userid = '{}';'''.format(str(date_val.__str__()),self.userid))
        values = self.cursor.fetchall()
        codes = []
        if (len(values)!=0):
            print("This are the values: ")
            for x in values:
                print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))
                codes.append(str(x[0]))
            print(codes)
            sesioncode = self.enterInteger()
            while (codes.count(str(sesioncode))==0):
                sesioncode = self.enterInteger()
            self.cursor.execute('''insert into sesionuser (userid,sesioncode)
            values('{}',{})'''.format(self.userid,str(sesioncode)))
        else:
            print("There are no available sesions for you at that hour ")
        
    def searchSesionByLength(self):
        print("Enter the amount of minutes ")
        date_val = datetime.time(0,self.enterInteger(),0)
        self.cursor.execute('''select * from sesion where timelength = '{}' 
        except all
        select sesion.sesioncode,sesion.sesionname,sesion.sesiondate,sesion.sesionhour,sesion.timelength,sesion.sesionstatus,sesion.description,sesion.workerid,sesion.categorycode from sesion
        inner join sesionuser 
        on sesionuser.sesioncode = sesion.sesioncode
        where userid = '{}';'''.format(str(date_val.__str__(),self.userid)))
        values = self.cursor.fetchall()
        codes = []
        if (len(values)!=0):
            print("This are the values: ")
            for x in values:
                print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))
                codes.append(str(x[0]))
            print(codes)
            sesioncode = self.enterInteger()
            while (codes.count(str(sesioncode))==0):
                sesioncode = self.enterInteger()
            self.cursor.execute('''insert into sesionuser (userid,sesioncode)
            values('{}',{})'''.format(self.userid,str(sesioncode)))
        else:
            print("There are no sesions with that length ")
    def searchSesionByInstructor(self):
        self.cursor.execute('''select * from worker where workertype = 'Instructor' ''')
        values = self.cursor.fetchall()
        id = []
        for x in values:
            print(''' Id:{}     Name:{} '''.format(str(x[0]),str(x[2])))
            id.append(str(x[0]))
        workerid = ""
        while True:
            workerid = input("Enter the id for the instructor: ")
            if (id.count(workerid)!=0):
                break
            print("The id entered is invalid, try again")
        self.cursor.execute('''select * from sesion where workerid = '{}' 
        except all
        select sesion.sesioncode,sesion.sesionname,sesion.sesiondate,sesion.sesionhour,sesion.timelength,sesion.sesionstatus,sesion.description,sesion.workerid,sesion.categorycode from sesion
        inner join sesionuser 
        on sesionuser.sesioncode = sesion.sesioncode
        where userid = '{}';'''.format(workerid,self.userid))
        values = self.cursor.fetchall()
        codes = []
        if (len(values)!=0):
            print("This are the values: ")
            for x in values:
                print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))
                codes.append(str(x[0]))
            print(codes)
            sesioncode = self.enterInteger()
            while (codes.count(str(sesioncode))==0):
                sesioncode = self.enterInteger()
            self.cursor.execute('''insert into sesionuser (userid,sesioncode)
            values('{}',{})'''.format(self.userid,str(sesioncode)))
        else:
            print("There are no available sesions for you with that instructor ")
    def getUserContract(self):
        self.cursor.execute('''select * from usercontract 
        inner join (select max(contractcode) 
        from usercontract 
        where userid = '{}') as p 
        on p.max = usercontract.contractcode'''.format(self.userid))
        values = self.cursor.fetchone()
        self.usercontract = UserContract(values)
    def saveUser(self):
        self.cursor.execute('''update usuario 
        set password = '{}',name = '{}', birthdate='{}',height = {},
        actualweight={},direction='{}' 
        where userid = '{}' '''.format(self.password,self.name,self.birthdate,self.height,self.actualweight,self.direction,self.userid))
    def logout(self):
        self.saveUser()
        self.cursor.close()
    def enterDate(self):
        while True:
            try:
                print("Enter the date year.")
                year = self.enterInteger()
                print("Enter the date month.")
                month = self.enterInteger()
                print("Enter the date day.")
                day = self.enterInteger()
                date_value = datetime.datetime(year,month,day)  
                if (date_value > date_value.now() ):
                    return date_value
            except:
                pass
            print("The date entered is invalid, please try again")
    def enterInteger(self):
        while True:
            try:
                return int(input("Enter the integer: "))
            except:
                print("The value entered is invalid, please try again")
    def showThisWeek(self):
        self.cursor.execute('''select sesion.sesionname,sesion.sesiondate,sesion.sesionhour,worker.workername from worker
        inner join sesion
        on worker.workerid = sesion.workerid
        inner join sesionuser
        on sesion.sesioncode = sesionuser.sesioncode
        where sesion.sesiondate<=current_date+interval '7 day'
        ''')
        print("For this week, these are your activities: ")
        values = self.cursor.fetchall()
        for x in values:
            print('''Name: {}       Date: {}        Hour: {}        Instructor: {}'''.format(x[0],x[1].__str__(),x[2].__str__(),x[3]))
    def showProfile(self):
        print('''Name: {}\nActual weight: {}\nBirthdate: {}\nHeight: {}\n'''.format(self.name, self.actualweight,self.birthdate,self.height))
    def showAnotherWeek(self):
        self.cursor.execute('''select sesion.sesionname,sesion.sesiondate,sesion.sesionhour,worker.workername from worker
        inner join sesion
        on worker.workerid = sesion.workerid
        inner join sesionuser
        on sesion.sesioncode = sesionuser.sesioncode
        where sesion.sesiondate<=current_date-interval '{} week'
        '''.format(self.enterInteger()))
        print("Para esta semana estas son las actividades: ")
        values = self.cursor.fetchall()
        for x in values:
            print('''Name: {}       Date: {}        Hour: {}        Instructor: {}'''.format(x[0],x[1].__str__(),x[2].__str__(),x[3]))
    def endSubscription(self,cursor):
        self.cursor.execute('''select now()+interval'2 min' ''')
        valid = self.cursor.fetchone()[0]
        cursor.execute('''alter user {} valid until '{}' '''.format(self.userid,valid))
    def statistics(self):
        self.cursor.execute('''select p.sesiondate,p.sesionhour,p.timelength,exercisetype,p.description,p.workername,userweight,heartrate,caloriesacomplished from sesionuser
        inner join (
            select sesioncode,sesionname,sesiondate,sesionhour,timelength,description,worker.workername
            from sesion
            inner join worker
            on worker.workerid = sesion.workerid
        ) as p
        on p.sesioncode = sesionuser.sesioncode
        where userid = '{}'; '''.format(self.userid))
        values = self.cursor.fetchall()
        for x in values:
            print('''
            Date: {}       Hour: {}        Length: {}
            Category: {}        Description: {}
            Instructor: {}      Heartrate: {}       Calories burned: {}\n'''.format(str(x[0].__str__()),str(x[1].__str__()),str(x[2].__str__()),str(x[3]),str(x[4]),str(x[5]),str(x[7]),str(x[8])))
    def historicWeight(self):
        self.cursor.execute('''select avg(userweight) from sesionuser where sesionuser.userid = '{}' '''.format(self.userid))
        mean = self.cursor.fetchone()
        self.cursor.execute('''select p.sesiondate,p.sesionhour,p.timelength,exercisetype,p.description,p.workername,userweight,heartrate,caloriesacomplished from sesionuser
        inner join (
            select sesioncode,sesionname,sesiondate,sesionhour,timelength,description,worker.workername
            from sesion
            inner join worker
            on worker.workerid = sesion.workerid
        ) as p
        on p.sesioncode = sesionuser.sesioncode
        where userid = '{}'; '''.format(self.userid))
        values = self.cursor.fetchall()
        for x in values:
            print('''
            Date: {}       Hour: {}        Length: {}
            Category: {}        Description: {}
            Weight: {}'''.format(str(x[0].__str__()),str(x[1].__str__()),str(x[2].__str__()),str(x[3]),str(x[4]),str(x[6])))
        print('''
            Average weight: {}'''.format(str(mean[0])))
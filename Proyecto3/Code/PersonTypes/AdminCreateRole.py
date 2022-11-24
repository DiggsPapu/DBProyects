
from PersonTypes.Worker import Worker
import random
class AdminCreateRole(Worker):
    def __init__(self, values) -> None:
        super().__init__(values=values)
    def createUser(self,username,password,name,birthdate,height,actualweight,direction,contractlength,subscriptiontype,paymentmethod,cardnumber):
        try:
            self.cursor.execute('''select (current_date + interval '{} month')::date'''.format(contractlength))
            expiration_date = self.cursor.fetchone()
            if (expiration_date!=  None):
                expiration_date = expiration_date[0]
            self.cursor.execute('''create user {} password '{}' valid until '{}'; 
            grant usuario to {};
            insert into usuario(userid,password,name,birthdate,height,actualweight,direction)
            values('{}','{}','{}','{}',{},{},'{}');
            insert into usercontract(userid,subscriptiontype,lastdate,paymentmethod,cardnumber)
            values('{}','{}','{}','{}',{})'''
            .format(username,password,expiration_date,
            username,
            username,password,name,birthdate,height,actualweight,direction,
            username,subscriptiontype,expiration_date,paymentmethod,cardnumber))
            self.cursor.execute("COMMIT")
        except:
            pass
    def createInstructor(self,username,password,name,direction,actualweight,height):
        try:
            self.cursor.execute('''select (current_date + interval '30 hour')''')
            expiration_date = self.cursor.fetchone()
            if (expiration_date!=  None):
                expiration_date = expiration_date[0]
            self.cursor.execute('''create user {} with password '{}' valid until '{}';
            grant instructor to {};
            insert into worker(workerid,workerpassword,workername,direction,workertype)
            values('{}','{}','{}','{}','Instructor');
            insert into instructorcontract(workerid,weight,height)
            values('{}',{},{})
            '''.format(username,password,expiration_date,
            username,
            username,password,name,direction,
            username,actualweight,height
            ))
            self.cursor.execute("COMMIT")
        except:
            pass
    def createAdminCreateRole(self, username,password,name,direction):
        self.cursor.execute('''create user {} with password '{}' createrole;
        grant admin_create_role to {};
        grant insert,select on worker to {};
        grant insert on instructorcontract to {};
        grant insert on sesionuser to {};
        grant insert,select on usuario to {};
        grant insert,select on usercontract to {};
        grant insert,select on bitacora to {};
        grant all privileges on all sequences in schema public to {};
        insert into worker(workerid,workerpassword,workername,direction,workertype)
        values('{}','{}','{}','{}','admin_create_role');'''
        .format(username,password,
        username,username,username,username,username,username,username,
        username,password,name,direction))
        self.cursor.close()
    def createAdminReportery(self,username,password,name,direction):
        self.cursor.execute('''create user {} with password '{}';
        grant admin_reportery to {};        
        insert into worker(workerid,workerpassword,workername,direction,workertype)
        values('{}','{}','{}','{}','admin_reportery')'''
        .format(username,password,
        username,username,username,
        username,password,name,direction))
class AdminReportery(Worker):  # type: ignore
    def __init__(self, values) -> None:
        super().__init__(values=values)
    def topTenSesions(self):
        self.cursor.execute('''select * from top_10_alltimesesions_user;''')
        values = self.cursor.fetchall()
        for x in values:
            print('''
            Date: {}        Hour: {}        Length: {}
            Category: {}        Sesion name: {}
            Amount of people who attended: {}\n
            '''.format(x[1].__str__(),x[2].__str__(),x[3].__str__(),x[5],x[0],str(x[6])))
    def topFiveSesions(self):
        self.cursor.execute('''select * from top_5_sesions_user;''')
        values = self.cursor.fetchall()
        for x in values:
            print('''
            Date: {}       Hour: {}        Length: {}
            Category: {}        Sesion name: {}
            Amount of people who attended: {}\n
            '''.format(x[1].__str__(),x[2].__str__(),x[3].__str__(),x[5],x[0],str(x[6])))    
    def topTenMostInstructor(self):
        self.cursor.execute('''select * from top_10_most_instructors;''')
        values = self.cursor.fetchall()
        for x in values:
            print('''
            Instructor: {}      Amount of people who search him: {}
            '''.format(x[0],str(x[1])))
    def subscriptionTypeLastSixMonthAmount(self):
        self.cursor.execute('''select * from subscriptiontype_lastsixmonth_amount;''')
        values = self.cursor.fetchall()
        for x in values:
            print('''
            Susbscription type: {}      Amount of people that acquire that subscription in the last 6 months: {}\n
            '''.format(x[0],str(x[1])))
    def picoHour(self,date):
        self.cursor.execute('''select count(uc.userid), s.sesionhour from sesion as s inner join (select userid, sesioncode from sesionuser) as uc on uc.sesioncode = s.sesioncode where s.sesiondate = '{}' group by s.sesionhour order by count(uc.userid) desc Limit 1'''.format(date))
        print("The pick hour is "+ str(self.cursor.fetchone()[1]))
    def usersWithoutEx(self):
        self.cursor.execute('''select * from users_withoutlast3week_exercise;''')
        values = (self.cursor.fetchall())
        if (len(values)==0):
            print("No user have not gone to classes in the last 3 weeks")
        else:
            for x in values:
                print('''
                User name: {}        Amount of abscences: {}\n
                '''.format(x[0],str(x[1])))
    

            
            
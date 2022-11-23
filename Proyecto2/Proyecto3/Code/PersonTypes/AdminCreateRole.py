
from PersonTypes.Worker import Worker


class AdminCreateRole(Worker):
    def __init__(self, values) -> None:
        super().__init__(values=values)
    def createUser(self,username,password,name,birthdate,height,actualweight,direction,contractlength,subscriptiontype,paymentmethod,cardnumber):
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
    def createInstructor(self,username,password,name,direction,actualweight,height):
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
        insert into worker(workerid,password,workername,workerdirection,workertype)
        values('{}','{}','{}','{}','admin_create_role');'''
        .format(username,password,
        username,username,username,username,username,username,username,
        username,password,name,direction))
        self.cursor.close()
    def createAdminReportery(self,username,password,name,direction):
        self.cursor.execute('''create user {} with password '{}';
        grant admin_reportery to {};        
        insert into(workerid,workerpassword,workername,direction,workertype)
        values('{}','{}','{}','{}','admin_reportery')'''
        .format(username,password,
        username,username,username,
        username,password,name,direction))

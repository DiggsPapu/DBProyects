from Objects.InstructorContract import InstructorContract
from PersonTypes.Worker import Worker
import datetime
class Instructor(Worker):  # type: ignore
    def __init__(self, values) -> None:
        super().__init__(values)
    def saveInstructor(self):
        self.cursor.execute('''update worker set workerid = '{}', workerPassword = '{}', workername = '{}', direction = '{}', workerType = '{}' where workerid = '{}' '''.format(self.worker_id, self.worker_password, self.worker_name, self.worker_direction, self.worker_type, self.worker_id))
    def renewContract(self,weight,height):
        self.cursor.execute('''select (current_date + interval '30 hour')''')
        expiration_date = self.cursor.fetchone()
        if (expiration_date!=  None):
            expiration_date = expiration_date[0]
        self.cursor.execute('''
        alter user {} password '{}' valid until '{}';
        insert into instructorcontract(workerid,contractlength,activecontract,weight,height)
        values('{}',{},{})'''.format(self.worker_id,self.worker_password,expiration_date,self.worker_id,weight,height))  
    def enterInteger(self):
        while True:
            try:
                return int(input("Enter the integer: "))
            except:
                print("The value entered is invalid, please try again")
    def enterTimeLength(self):
        while True:
            try:
                min = int(input("Enter the minutes of the sesion: "))
                if (min<=59):
                    return datetime.time(0,min,0)
                print("The amount of minutes of sesion is too long")
            except:
                print("The value entered is not valid, try again")
    def enterDate(self):
        while True:
            try:
                print("Enter the date year.")
                year = self.enterInteger()
                print("Enter the date month.")
                month = self.enterInteger()
                print("Enter the date day.")
                day = self.enterInteger()
                print("Enter the date hour.")
                hour = self.enterInteger()
                date_value = datetime.datetime(year,month,day,hour)  
                if (date_value > date_value.now() and hour>=5 and hour <=22):
                    self.cursor.execute('''select count(workerid) from sesion where sesiondate = '{}' and sesionhour = '{}' and workerid = '{}' '''.format(date_value.date(),date_value.time(),self.worker_id))
                    val = self.cursor.fetchone()
                    val = val[0]
                    if (val>0):
                        print("At that date and hour you have an apointment in another sesion, please enter another date")
                    else:
                        return date_value
            except:
                print("The date entered is invalid, please try again")
                pass
    def newSesion(self):
        name = input("Enter the sesion name: ")
        date_val = self.enterDate()
        self.cursor.execute('''select category from excategory''')
        print("These are the categories: ")
        values = self.cursor.fetchall()
        if (len(values)!=0):
            valores = []
            count = 0
            for x in values:
                valores.append(x[0])
                print(str(count)+"- "+str(valores[count]))
                count+=1
            pro = True
            option = input("Enter the number of the category: ")
            while (pro):
                try:
                    if (0<=int(option) and int(option)<count):
                        pro = False
                        break
                    else:
                        print("The option entered doesn't exist")
                except:
                    print("The value entered is invalid")
                option = input("Enter the number of the category: ") 
            timelength = self.enterTimeLength()
            self.cursor.execute('''select categorycode from excategory where category = '{}' '''.format(str(valores[int(option)])))
            category_code = self.cursor.fetchone()
            category_code = category_code[0]
            self.cursor.execute('''insert into sesion(sesionname,sesiondate,sesionhour,sesionstatus,timelength,description,workerid,categorycode)
            values('{}','{}','{}','WAIT','{}','{}','{}',{})'''.format(name,str(date_val.date()),str(date_val.time()),timelength.__str__(),input("Enter the description of the sesion: "),self.worker_id,str(category_code)))
        else:
            print("There are no categories yet")
    def newCategory(self,category_name):
        self.cursor.execute('''insert into excategory(category) values('{}')'''.format(category_name))
    def deleteCategory(self,category_name):
        self.cursor.execute('''delete from excategory where excategory.category = '{}' '''.format(category_name))
    def dropSesion(self):
        self.cursor.execute('''select * from sesion where workerid = '{}' '''.format(self.worker_id))
        values = self.cursor.fetchall()
        count = 1
        for x in values:
            print('''{}- Name: {}       Date:{}     Hour: {}        Length: {}      Status: {}      Description: {}'''.format(str(x[0]),str(x[1].__str__()),str(x[2].__str__()),str(x[3].__str__()),str(x[4]),x[5],x[6]))
            count+=1
        sesioncode = self.enterInteger()
        while (sesioncode<1 or sesioncode>count):
            sesioncode = self.enterInteger()
        self.cursor.execute('''delete from sesion where sesioncode = {} '''.format(str(values[sesioncode-1][0])))
    def logout (self):
        self.saveInstructor()
        self.cursor.close()
    def getInstructorContract(self):
        self.cursor.execute('''select * from instructorcontract
        inner join (select max(contractinstructorcode) from instructorcontract where workerid = '{}') as p
        on p.max = instructorcontract.contractinstructorcode '''.format(self.worker_id))
        values = self.cursor.fetchone()
        self.instructor_contract = InstructorContract(values)
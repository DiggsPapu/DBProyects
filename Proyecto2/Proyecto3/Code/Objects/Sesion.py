from Proyecto3.Code.ConectDB import connectDB
from Proyecto3.Code.GlobalFunctions import *


class Sesion:
    def __init__(self,values) -> None:
        self.code = str(values[0])
        self.name = str(values[1]),
        self.date = str(values[2]),
        self.hour = str(values[3]),
        self.time_length = str(values[4]),
        self.status = str(values[5]),
        self.description = str(values[6]),
        self.worker_id = str(values[7]),
        self.category_code = str(values[8]),
        self.cursor = connectDB()
    def updateLocalValues(self):
        self.cursor.execute('''select * from sesion where sesioncode = {}'''.format(self.code))
        values = self.cursor.fetchone()
        if (values!=None):
            values = values[0]
            self.code = str(values[0])
            self.name = str(values[1]),
            self.date = str(values[2]),
            self.hour = str(values[3]),
            self.time_length = str(values[4]),
            self.status = str(values[5]),
            self.description = str(values[6]),
            self.worker_id = str(values[7]),
            self.category_code = str(values[8]),
    def sesionUpdate(self):
        self.cursor.execute('''update sesion set sesionname = '{}', sesiondate = '{}', sesionhour = {}, timelength = {}, sesionstatus = '{}', description = '{}', workerid = {}, categorycode = {} '''.format(self.code, self.name, self.date, self.hour, self.time_length,self.status,self.description,self.worker_id,self.category_code))
    def nameSesionUpdate(self):
        name = enterSesionName()
        self.name = name
        self.sesionUpdate()
    def dateSesionUpdate(self):
        date = enterDate()
        self.date = date
        self.sesionUpdate()
    def hourSesionUpdate(self):
        hour = enterHour()
        self.hour = hour
        self.sesionUpdate()
    def lengthSesionUpdate(self):
        length = enterSesionLength()
        self.time_length = length
        self.sesionUpdate()
    def statusSesionUpdate(self):
        status = enterSesionStatus()
        self.status = status
        self.sesionUpdate()
    def descriptionSesionUpdate(self):
        description = input("Enter new description: ")
        self.description = description
        self.sesionUpdate()
    def instructorSesionUpdate(self):
        instructor = printAndSelectInstructor(self.cursor)
        self.worker_id = instructor
        self.sesionUpdate()
    def categorySesionUpdate(self):
        category = printAndSelectCategory(self.cursor)
        self.category_code = category
        self.sesionUpdate()
    
    
    
import maskpass
import datetime
def enterWorkerType():
    while (True):
        workerType = input("Enter the worker type between:\n1- Admin\n2- Instr\n")
        if (workerType=="1"):
            return "Admin" 
        elif (workerType == "2"):
            return "Instr"
        print("The entered value is invalid.\n")
def enterSomething(something):
    while (True):
        calories = input("Enter the amount of {}: ".format(something))
        try:
            float(calories)
            return calories
        except: print("The amount of {} entered is invalid.\n".format(something))

def enterWeight():
    while (True):
        try: 
            weight = float(input("Enter your weight in kg: "))
            if (25<=weight and 700>=weight):
                return weight
            float("hola") #Para lanzar el error por valor invalido
        except:
            print("Incorrect enter of weight, please try again.\n\n")
def enterHeight():
    while (True):
        try: 
            height = float(input("Enter your height in mts: "))
            if (0.5<=height and 3.0>=height):
                return height
            float("hola") #Para lanzar el error por valor invalido
        except:
            print("Incorrect enter of height, please try again.\n\n")
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
            if (int(birthdateAr[0])>=1940):
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
def enterName():
    while (True):
        name = input("Enter your name: ") 
        if (len(name)<=30):
            return name
        print("The entered named is too long.\n")

def enterSesionStatus():
    while (True):
        status = input("Enter the sesion status between:\n1- Wait\n2- Done\n3- Cancelled\n")
        if (status=="1"):
            return "wait"
        elif (status == "2"):
            return "done"
        elif (status == "3"):
            return "canc"
        else:
            print("The entered value is invalid.\n")

def checkSesionHourAvailability(workerid, cursor):
    while (True):
        date = enterDate()
        hour = enterHour()
        cursor.execute('''select count(sesioncode) from sesion where workerid = '''+str(workerid)+''' and sesiondate = \''''+date+'''\' and sesionhour = \''''+hour+'''\'''')
        if (int(cursor.fetchone()[0])==0):
            facts = [date, hour]
            return facts
        else:
            print("The hour and date entered is already reserved for this instructor.\n")
def printAndSelectCategory(cursor):
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
def enterPassword():
    while (True):
        password = maskpass.askpass(prompt="Enter password: ", mask="*")
        confirmp = maskpass.askpass(prompt="Reenter password: ", mask="*")
        if (confirmp== password):
            return password
        print("The passwords don't match, please try again.\n\n")

def enterBirthDate():
    while (True):
        birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
        birthdateAr = birthdate.split("-")
        try:
            datetime.datetime(int(birthdateAr[0]),int(birthdateAr[1]),int(birthdateAr[2]) )
            if (int(birthdateAr[0])>1930):
                return birthdate
            print("Your birthdate doesn't make sense, nobody is that old please try again.\n\n")
        except:
            print("Incorrect data format, should be YYYY-MM-DD, please try again.\n\n")
def enterSubscription(initdate):
    subscription = []
    while (True):
        option = input("Select between:\n1- Gold subscription, costs Q. 250.00 per month.\n2- Diamond subscription, costs Q. 500.00 per month.\n")
        if (option == "1"):
            subscription.append("Gold")
            while(True):
                option = input("Enter the amount of months of the contract, remember that at least is 12 months per contract: ")
                try: 
                    if (int(option)>=12):
                        idate = initdate.split("-")
                        if ( int(option)%12==0):
                            idate[0]=str(int(int(idate[0])+int(option)/12))
                        else:
                            idate[0] = str(int((int(option)+int(idate[1]))/12)+int(idate[0]))
                            if (int((int(option)+int(idate[1]))%12)==0):
                                idate[1]="12"
                            elif(int((int(option)+int(idate[1]))%12)<10):
                                idate[1]="0"+str(int((int(option)+int(idate[1]))%12))
                            else:
                                idate[1]=str(int((int(option)+int(idate[1]))%12))
                        initdate = idate[0]+"-"+idate[1]+"-"+idate[2]
                        print("The last date of use is: "+initdate)
                        subscription.append(initdate)
                        return subscription
                    int("hola")
                except:
                    print("The amount of months is invalid.\n")            
        elif (option == "2"):
            subscription.append("Diamond")
            while(True):
                option = input("Enter the amount of months of the contract, remember that at least is 12 months per contract: ")
                try: 
                    if (int(option)>=12):
                        idate = initdate.split("-")
                        if ( int(option)%12==0):
                            idate[0]=str(int(int(idate[0])+int(option)/12))
                        else:
                            idate[0] = str(int((int(option)+int(idate[1]))/12)+int(idate[0]))
                            if (int((int(option)+int(idate[1]))%12)==0):
                                idate[1]="12"
                            elif(int((int(option)+int(idate[1]))%12)<10):
                                idate[1]="0"+str(int((int(option)+int(idate[1]))%12))
                            else:
                                idate[1]=str(int((int(option)+int(idate[1]))%12))
                        initdate = idate[0]+"-"+idate[1]+"-"+idate[2]
                        print("The last date of use is: "+initdate)
                        subscription.append(initdate)
                        return subscription
                    int("hola")
                except:
                    print("The amount of months is invalid.\n")
        else:
            print("The value entered is invalid.\n\n")
def enterCardNumber():
    while (True):
        cardNumber = input("Enter your card number, remember that a card  number has 16 digits: ")
        correctCard = True
        for x in cardNumber:
            try:
                int(x)
            except:
                correctCard = False
        if (correctCard and len(cardNumber)==16):
            return cardNumber
        else:
            print("The card enter is invalid") 
def getSesion(cursor):
    print("The date to search the sesion wanted is needed.\n")
    date = enterDate()
    cursor.execute('''select * from sesion where sesiondate = \'{}\' and sesionstatus = \'wait\''''.format(date))
    sesions = cursor.fetchall()
    value = 0
    print("Select between this: ")
    for x in sesions:
        print(str(value)+"- Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Hour: "+str(x[3])+" Description: "+str(x[6]))
        value+=1
    sesion = ""
    while (True):
        sesion = input("Enter sesion selected: ")
        try:
            sesion = sesions[int(sesion)]
            print(sesion)
            return sesion
        except:
            print("The selected sesion is invalid, try again.\n")
def deleteSesion(cursor):
    sesion = getSesion(cursor)
    query = '''delete from sesion where sesioncode = {} and sesionstatus != \'done\''''.format(sesion[0])
    cursor.execute(query)
def enterSesionLength():
     while (True):
        hour = input("Enter the sesion length (HH:MM:SS), remember that it must be between 30 and 60 min long: ")
        hourAr = hour.split(":")
        try:
            if (int(hourAr[0])==0 and 30<=int(hourAr[1])<60 and 0<=int(hourAr[2])<60):
                return hour
            print("The sesion length entered is invalid, please try again.\n")
        except:
            print("The sesion length entered is invalid, please try again.\n")
def printAndSelectInstructor(cursor):
    while (True):
        cursor.execute('''select * from worker where workertype = 'Instr' ''')
        instructors = cursor.fetchall()
        print("These are the instructors: \n")
        for x in instructors:
            print("id: "+str(x[0])+" name: "+ str(x[2]))
        id = input("Enter the instructor id: ")
        try:
            int(id)
            cursor.execute('''select * from worker where workerid = {} and workertype = \'Instr\''''.format(id))  
            instructor = cursor.fetchone()
            return instructor
        except:
            print("The id entered is invalid.\n")
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

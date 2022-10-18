import maskpass
import datetime
from InstructorFunctions import *
def loggedInAdmin(username, password,cursor):
    search = '''select * from worker
    where workerid='''+username+''' and workerpassword =\''''+password+'''\' and workertype= \'Admin\''''
    cursor.execute(search)
    admin = cursor.fetchone()
    if (admin!=None):
        while (True):
            option = input('''Welcome back admin '''+str(admin[2])+'''!\nWhat do you want to do today?\n1- Update user information\n2- Grant user access, cancel user access or renewal user contract.\n3- Create new sesion\n4- Update sesion information\n5- Delete a sesion\n6- Renew instructor contract\n7- Add a new instructor\n8- Update instructor information\n9- Quit an instructor\n10- Create a category\n11- Delete a category\n12- Create a new admin\n13- Exit\n''')
            if (option == "1"):
                updateUserInfo(cursor)
            elif (option == "2"):
                changeUserAccess(cursor)
            elif (option == "3"):
                createSesion(cursor)
            elif (option == "4"):
                updateSesionInfo(cursor)
            elif (option == "5"):
                deleteSesion(cursor)
            elif (option == "6"):
                renewalContract(getInstructor(cursor)[0],cursor)
            elif (option == "7"):
                createInstructor(cursor=cursor)
            elif (option == "8"):
                updateInstructorInfo(cursor)
            elif (option == "9"):
                quitInstructor(cursor)
            elif (option == "10"):
                createCategory(cursor)
            elif (option == "11"):
                deleteCategory(cursor)
            elif (option == "13"):
                break
            else:
                print("The option entered is invalid.\n")
def updateSesionInfo(cursor):
    sesion = getSesion(cursor)
    updatingwant = True
    while (updatingwant):
        option = input('''Select what column do you want to update:\n1- Sesion name\n2- Sesion hour\n3- Sesion time length\n4- Sesion status\n5- Sesion description\n6- Sesion instructor\n7- Sesion category\n8- Exit\n''')
        updatequery = '''update sesion set {} = \'{}\' where sesioncode = {}'''
        if (option == "1"): 
            name = enterSesionName()
            cursor.execute(updatequery.format("sesionname", name, sesion[0]))
        elif (option == "2"):
            hour = enterHour()
            cursor.execute(updatequery.format("sesionhour", hour, sesion[0]))
        elif (option == "3"):
            hour = sesionLength()
            cursor.execute(updatequery.format("timelength", hour, sesion[0]))
        elif (option == "4"):
            hour = enterSesionStatus()
            cursor.execute(updatequery.format("sesionstatus", hour, sesion[0]))
        elif (option == "5"):
            hour = input("Enter new description: ")
            cursor.execute(updatequery.format("description", hour, sesion[0]))
        elif (option == "6"):
            hour = getInstructor(cursor)
            cursor.execute(updatequery.format("workerid", hour[0], sesion[0]))
        elif (option == "7"):
            hour = getCategory(cursor)
            cursor.execute(updatequery.format("categorycode", hour[0], sesion[0]))
        elif (option == "8"):break
        else:print("The option entered is invalid.\n")
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
    
def updateInstructorInfo(cursor):
    instructor = getInstructor(cursor)
    while (instructor == None):
        print("The instructor id entered was not correct\n")
        instructor = getInstructor(cursor)
    updatingwant = True
    while (updatingwant):
        option = input('''\n\nSelect what column do you want to update:\n1- Worker password\n2- Worker name\n3- Worker direction\n4- Exit\n''')
        updatequery = '''update worker set {} = {} where workerid = {}'''
        if (option == "1"):
            password = enterPassword()
            updatequery = updatequery.format("workerpassword","\'"+password+"\'",instructor[0])
            cursor.execute(updatequery)
        elif (option == "2"):
            name = enterName()
            updatequery = updatequery.format("workername","\'"+name+"\'",instructor[0])
            cursor.execute(updatequery)
        elif (option == "3"):
            direction = input("Enter the direction: ")
            updatequery = updatequery.format("direction","\'"+direction+"\'",instructor[0])
            cursor.execute(updatequery)
        elif (option == "4"):
            break
        else:
            print("The option entered was invalid.\n")
def createSesion(cursor):
    instructor = getInstructor(cursor)
    while (instructor == None):
        print("The instructor entered, was invalid: ")
        instructor = getInstructor(cursor)
    workerid = instructor[0]
    cursor.execute('''select max(sesioncode) from sesion''')
    contractcode = ""
    contractcode = cursor.fetchone()[0]
    if (contractcode!=None):
        contractcode = str(int(contractcode)+1)
    else:
        contractcode = "0"
    sesionname = enterSesionName()
    time = checkHour(workerid=workerid, cursor=cursor)
    sesionDate = time[0]
    sesionHour = time[1]
    sesionlength = sesionLength()
    description = input("Describe what is the sesion about: ")
    categorycode = getCategory(cursor)
    configureSesion = '''insert into sesion(
        sesioncode,sesionname,sesiondate,sesionhour,
        timelength,
        sesionstatus,description,workerid,categorycode
    )
    values(
        '''+str(contractcode)+''',
        \''''+str(sesionname)+'''\',
        \''''+str(sesionDate)+'''\',
        \''''+str(sesionHour)+'''\',
        \''''+str(sesionlength)+'''\',
        \'wait\',
        \''''+str(description)+'''\',
        '''+str(workerid)+''',
        '''+str(categorycode)+'''
    )
    '''
    cursor.execute(configureSesion)
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
        
def sesionLength():
     while (True):
        hour = input("Enter the sesion length (HH:MM:SS), remember that it must be between 30 and 60 min long: ")
        hourAr = hour.split(":")
        try:
            if (int(hourAr[0])==0 and 30<=int(hourAr[1])<60 and 0<=int(hourAr[2])<60):
                return hour
            print("The sesion length entered is invalid, please try again.\n")
        except:
            print("The sesion length entered is invalid, please try again.\n")
def updateUserInfo(cursor):
    user = getUser(cursor)
    while (user==None):
        print("The user id entered was not correct\n")
        user = getUser(cursor)
    updatingwant = True
    while (updatingwant):
        option = input('''Select what column do you want to update:\n1- User password\n2- User name\n3- User birthdate\n4- User height\n5- User weight\n6- User direction\n7- Exit\n''')
        updatequery = '''update usuario set {} = {} where userID = {}'''
        if (option == "1"):
            password = enterPassword()
            updatequery = updatequery.format("password","\'"+password+"\'", "\'"+user[0]+"\'")
            cursor.execute(updatequery)
        elif (option == "2"):
            password = enterName()
            updatequery = updatequery.format("name","\'"+password+"\'", "\'"+user[0]+"\'")
            cursor.execute(updatequery)
        elif (option == "3"):
            password = enterBirthDate()
            updatequery = updatequery.format("birthdate","\'"+password+"\'", "\'"+user[0]+"\'")
            cursor.execute(updatequery)
        elif (option == "4"):
            password = enterHeight()
            updatequery = updatequery.format("height",password, "\'"+user[0]+"\'")
            cursor.execute(updatequery)
        elif (option == "5"):
            password = enterWeight()
            updatequery = updatequery.format("actualweight",password,"\'"+user[0]+"\'")
            cursor.execute(updatequery)
        elif (option == "6"):
            password = input("Enter the new direction: ")
            updatequery = updatequery.format("direction","\'"+password+"\'", "\'"+user[0]+"\'")
            cursor.execute(updatequery)
        elif (option == "7"):
            updatingwant = False
        else:
            print("The entered option is invalid.\n")

def quitInstructor(cursor):
    id = str(getInstructor(cursor)[0])
    while (id==None):
        print("The instructor id entered was not correct\n")
        id = str(getInstructor(cursor)[0])
    cursor.execute('''select max(contractinstructorcode) from instructorcontract where workerid = {}'''.format(id[0]))
    getcontractcode = str(cursor.fetchone()[0])
    query = '''update instructorcontract set activecontract = False where contractinstructorcode = {}'''.format(getcontractcode)
    cursor.execute(query)
def getInstructor(cursor):
    while (True):
        id = input("Enter the instructor id: ")
        try:
            int(id)
            cursor.execute('''select * from worker where workerid = {} and workertype = \'Instr\''''.format(id))  
            instructor = cursor.fetchone()
            return instructor
        except:
            print("The id entered is invalid.\n")
def changeUserAccess(cursor):
    while (True):
        option = input("1- Grant user access\n2- Cancel user access\n")
        if (option == "1"):
            user = getUser(cursor)
            while (user==None):
                print("The user id entered was not correct\n")
                user = getUser(cursor)
            cursor.execute('''select max(contractcode) from usercontract where userid = \'{}\''''.format(user[0]))
            getcontractcode = str(cursor.fetchone()[0])
            query = '''update usercontract set activecontract = True where contractcode = {}'''.format(getcontractcode)
            cursor.execute(query)
            break
        elif(option == "2"):
            user = getUser(cursor)
            while (user==None):
                print("The user id entered was not correct\n")
                user = getUser(cursor)
            cursor.execute('''select max(contractcode) from usercontract where userid = \'{}\''''.format(user[0]))
            getcontractcode = str(cursor.fetchone()[0])
            query = '''update usercontract set activecontract = False where contractcode = {}'''.format(getcontractcode)
            cursor.execute(query)
            break
        elif (option == "3"):
            user = getUser(cursor)
            while (user==None):
                print("The user id entered was not correct\n")
                user = getUser(cursor)
            createUserContract(user[0], cursor)
        else:
            print("The option enter in invalid\n")   
def getUser(cursor):
    username = input("Enter the user id: ")
    searchUser = '''select * from usuario where userid=\''''+username+'''\''''
    cursor.execute(searchUser)
    value = cursor.fetchone()
    if (value!=None):
        return value
    else: return None
def checkUserName(cursor):
    while (True):
        username = input("Enter your username: ") 
        cursor.execute('''select count(userid) from usuario where userid = \''''+username+'''\'''')
        if (cursor.fetchone()[0]!=0):
            print("This username is already taken, please try again.\n")
        else:
            return username
def createUser(cursor):
    username = checkUserName(cursor=cursor)
    name = enterName()
    password = enterPassword() 
    birthdate = enterBirthDate() 
    height = enterHeight() 
    weight = enterWeight() 
    direction = input("Enter your direction: ")
    insertNewUser ='''insert into usuario(
        userid,password,
        name,birthdate,
        height,actualweight,
        direction
        ) 
        values(\''''+username+'''\',\''''+password+'''\',
        \''''+name+'''\',\''''+birthdate+'''\','''+str(height)+''',
        '''+str(weight)+''',\''''+direction+'''\')'''
    cursor.execute(insertNewUser)
    createUserContract(username=username, cursor=cursor)
def enterName():
    while (True):
        name = input("Enter your name: ") 
        if (len(name)<=30):
            return name
        print("The entered named is too long.\n")
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

def enterHeight():
    while (True):
        try: 
            height = float(input("Enter your height in mts: "))
            if (0.5<=height and 3.0>=height):
                return height
            float("hola") #Para lanzar el error por valor invalido
        except:
            print("Incorrect enter of height, please try again.\n\n")

def enterWeight():
    while (True):
        try: 
            weight = float(input("Enter your weight in kg: "))
            if (25<=weight and 700>=weight):
                return weight
            float("hola") #Para lanzar el error por valor invalido
        except:
            print("Incorrect enter of weight, please try again.\n\n")

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
def enterPaymentMethod():
    while (True):
        option = input("Select the payment method between:\n1- Credit card\n2- Debit card\n")
        if (option == "1"):
            return "Credit"
        elif (option == "2"):
            return "Debit"
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
           
def searchInstructor(username, password, cursor):
    try:
        int(username)
        searchUser = '''select * from worker where workerid='''+username+''' and workerpassword =\''''+password+'''\' and workertype = \'Instr\''''
        cursor.execute(searchUser)
        value = cursor.fetchone()
        if (value!=None):
            return value
        else: return None
    except:
        return None
def enterDate():
    while (True):
        birthdate = input("Enter date (YYYY-MM-DD): ")
        birthdateAr = birthdate.split("-")
        try:
            datetime.datetime(int(birthdateAr[0]),int(birthdateAr[1]),int(birthdateAr[2]) )
            return birthdate
        except:
            print("Incorrect data format, should be YYYY-MM-DD, please try again.\n\n")
def createUserContract(username, cursor):
    print("We need the date of subscription init.\n")
    initdate = enterDate()
    subscriptionSpecifications = enterSubscription(initdate)
    subscriptionType = subscriptionSpecifications[0]
    subscriptionLength = subscriptionSpecifications[1]
    payMethod = enterPaymentMethod()
    cardNumber = enterCardNumber()
    cursor.execute('''select max(contractcode) from usercontract''')
    getNumberContract = cursor.fetchone() #Returns a tuple
    smartwatchReturn = True
    if (subscriptionType =="Gold"):
        smartwatchReturn = True
    elif(subscriptionType=="Diamond"):
        smartwatchReturn = False
    insertNewContractUser = '''insert into usercontract(
        contractcode,userid,subscriptiontype,lastdate,
        smartwatchreturn,activecontract,
        paymentmethod,cardnumber,initdate
    )
    values('''+str(int(getNumberContract[0])+1)+''',
        \''''+username+'''\',
        \''''+subscriptionType+'''\',
        \''''+str(subscriptionLength)+'''\',
        '''+str(smartwatchReturn)+''',true,
        \''''+payMethod+'''\',\''''+cardNumber+'''\',
        \''''+initdate+'''\')'''
    cursor.execute(insertNewContractUser)
def searchAdmin(username, password, cursor):
    try:
        int(username)
        searchUser = '''select * from worker where workerid='''+username+''' and workerpassword =\''''+password+'''\' and workertype = \'Admin\''''
        cursor.execute(searchUser)
        value = cursor.fetchone()
        if (value!=None):
            return value
        else: return None
    except:
        return None
def searchUser(username, password, cursor):
    searchUser = '''select * from usuario where userid=\''''+username+'''\' and password =\''''+password+'''\''''
    cursor.execute(searchUser)
    value = cursor.fetchone()
    if (value!=None):
        return value
    else: return None
def createInstructor(cursor):
    cursor.execute('''select max(workerid) from worker''')
    workerid = str(int(cursor.fetchone()[0])+1)    
    password = enterPassword()
    workerName = enterName()
    direction = input("Enter your direction: ")
    createInstructor = '''insert into worker(
        workerid, workerpassword,workername,
        direction,workertype)
    values(
        '''+workerid+''',
        \''''+password+'''\',
        \''''+workerName+'''\',
        \''''+direction+'''\',
        \'Instr\')
    '''
    cursor.execute(createInstructor)
    renewalContract(workerid=workerid, cursor=cursor)
def renewalContract(workerid, cursor):
    cursor.execute('''select max(contractinstructorcode) from instructorcontract''')
    contractcode = str(int(cursor.fetchone()[0])+1)
    weight = enterWeight()
    height = enterHeight()
    createContract = '''insert into instructorcontract(
        contractinstructorcode,workerid,contractlength,
        activecontract,weight,height
    )
    values(
        '''+contractcode+''',
        '''+str(workerid)+''',
        30,True,
        '''+str(weight)+''',
        '''+str(height)+'''               
    )
    '''
    cursor.execute(createContract)  
def enterWorkerType():
    while (True):
        workerType = input("Enter the worker type between:\n1- Admin\n2- Instr\n")
        if (workerType=="1"):
            return "Admin" 
        elif (workerType == "2"):
            return "Instr"
        print("The entered value is invalid.\n")

def createCategory(cursor):
    cursor.execute('''select max(categorycode) from excategory''')
    amountCategory = cursor.fetchone()[0]
    if (amountCategory == None):
        amountCategory = "0"
    while (True):
        category = input("Enter the new category (must have less than 31 letters): ")
        if (len(category)>30):
            print("The category entered is invalid, try again.\n")
        else:
            insertCategory = '''insert into excategory(
                categorycode, category
            )
            values(
                '''+str(int(amountCategory)+1)+''',
                \''''+category+'''\'
            )
            '''
            cursor.execute(insertCategory)
            break
def deleteCategory(cursor):
    category = input("Enter the category to be deleted: ")
    cursor.execute('''delete from excategory where category=\''''+category+'''\'''')
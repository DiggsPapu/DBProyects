import maskpass
import datetime
from Connection.ConectDB import *
from PersonTypes.AdminCreateRole import *
from PersonTypes.Instructor import Instructor
from PersonTypes.User import User
import names
def reporteryMenu(admin:AdminReportery)->None:
    while (True):
        option = input('''Welcome {}\n1- Check top 10 sesions from all time\n2- Check top 5 sesions between 9 and 18 hrs\n3- Top 10 most wanted instructors\n4- Top 20 users that havent been doing exercise since 3 weeks ago\n5- Amount of accounts created classified by types in the last 6 months\n6- Pico hour\n7- Simulate operation\n8- Exit\n'''.format(admin.worker_name))
        if (option == "1"):
            admin.topTenSesions()
        elif (option == "2"):
            admin.topFiveSesions()
        elif (option == "3"):
            admin.topTenMostInstructor()
        elif (option == "4"):
            admin.usersWithoutEx()
        elif (option == "5"):
            admin.subscriptionTypeLastSixMonthAmount()
        elif (option == "6"):
            admin.picoHour(enterDate(admin.cursor))
        elif (option == "7"):
            simulateOperations()
        elif (option == "8"):
            break
def createRoleMenu(admin:AdminCreateRole)->None:
    while (True):
        option = input('''Welcome {}\n1- Create user\n2- Create instructor\n3- Create admin reportery\n4- Exit\n'''.format(admin.worker_name))
        if (option == "1"):
            admin.createUser(enterNewUsername(admin.cursor),maskpass.askpass("Enter new password: ","*"),input("Enter name: "),enterBirthdate(),enterHeight(),enterWeight(),input("Enter direction: "),enterContractLenght(),enterSubscriptionType(),enterPaymentMethod(),enterCardNumber())
        elif (option == "2"):
            admin.createInstructor(enterNewUsername(admin.cursor),maskpass.askpass("Enter new password: ","*"),input("Enter name: "),input("Enter the direction: "),enterWeight(),enterHeight())
        elif (option == "3"):
            admin.createAdminReportery(enterNewUsername(admin.cursor),maskpass.askpass("Enter new password: ","*"),input("Enter name: "),input("Enter the direction: "))
        elif (option == "4"):
            print("Thanks for using the app admin")
            admin.cursor.close()
            break
def selectDropSesion(user:Instructor):
    user.cursor.execute('''select * from sesion where current_date<sesiondate and workerid = '{}' '''.format(user.worker_id))
    values = cursor.fetchall()
    count = 0
    for x in values:
        print(str(count) +" "+x)
    try:
        option = int(input('''Enter the option: '''))
        if (option>=0 and option<count):
            return option
    except:
        pass
    print('''The option enter is invalid''')
    return None
def enterDate(cursor):
    cursor.execute('''select current_date;''')
    actual_date = cursor.fetchone()[0]
    birthdate = input("Enter sesion date (YYYY-MM-DD): ")
    birthdateAr = birthdate.split("-")
    try:
        date = datetime.date(int(birthdateAr[0]),int(birthdateAr[1]),int(birthdateAr[2]) )
        if (date>=actual_date):
            return birthdate
        print('''Your sesion date doesn't make sense''')
        return None
    except:
        print('''Incorrect data format, should be YYYY-MM-DD''')
        return None
def enterHour():
    while (True):
        hour = input("Enter the hour (HH:MM:SS): ")
        hourAr = hour.split(":")
        try:
            if (0<=int(hourAr[0])<=22 and 0<=int(hourAr[1])<60 and 0<=int(hourAr[2])<60):
                return hour
            print("The hour entered is invalid, please try again.\n")
        except:
            print("The hour entered is invalid, please try again.\n")
def userMenu(user:User)->None:
    while (True):
        option = input('''Welcome {}\nSelect between this options:\n1- Search a sesion\n2- This week calendary\n3- Historic search\n4- Statistics\n5- End subscription\n6- Profile\n7- Change actual weight \n8- Historic weight\n9- Logout\n'''.format(user.name))
        if (option == '1'):
            while True:
                option = input("Select between this search type:\n1- Date\n2- Hour\n3- Length\n4- Instructor name\n5- Close\n")
                if (option =="1"):
                    user.searchSesionByDate()
                elif (option == "2"):
                    user.searchSesionByHour()
                elif (option == "3"):
                    user.searchSesionByLength()
                elif (option == "4"):
                    user.searchSesionByInstructor()
                elif (option == "5"):
                    break
        elif(option == "2"):
            user.showThisWeek()
        elif(option == "3"):        
            print("How many weeks ago?")
            user.showAnotherWeek()
        elif (option == "4"):
            user.statistics()
        elif (option == "5"):
            user.endSubscription(connectAdmin("postgres","Manager123"))
        elif(option == "6"):
            user.showProfile()
        elif(option == "7"):
            user.actualweight = enterWeight()
            print(user.userid)
            print(user.actualweight)
            user.saveUser()
        elif (option == "8"):
            user.historicWeight()
        elif(option == "9"):
            print('''{} thanks for using our app'''.format(user.name))
            user.logout()
            break
def showCategories(user):
    user.cursor.execute('''select category from excategory''')
    print("These are the categories: ")
    values = user.cursor.fetchall()
    valores = []
    count = 0
    for x in values: 
        valores.append(x[0])
        print(str(count)+" "+str(valores[count]))
        count+=1
    return count
def selectTime(user:Instructor):
    print("Please enter the date you want to assign the sesion.")
    date = enterDate(user.cursor)
    print("Please enter the hour you want to assign the sesion.")
    hour = enterHour()
    user.cursor.execute('''select count(workerid) from sesion where workerid = '{}' and sesionhour ='{}' and sesiondate = '{}' '''.format(user.worker_id,hour,date))
    if (user.cursor.fetchone()[0]==0):
        return [hour,date]
    return None
def selectCategory(user):
    user.cursor.execute('''select category from excategory''')
    print("These are the categories: ")
    values = user.cursor.fetchall()
    valores = []
    count = 0
    for x in values:
        valores.append(x[0])
        print(str(count)+" "+str(valores[count]))
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
    user.cursor.execute('''select categorycode from excategory where category = '{}' '''.format(str(valores[int(option)])))
    return user.cursor.fetchone()[0]
def instructorMenu(user:Instructor)->None:
    while (True):
        option = input('''Welcome {}\nSelect between this options:\n1- Profile\n2- Edit profile\n3- Create sesion\n4- Delete sesion\n5- Create category\n6- Logout\n'''.format(user.worker_name))
        if (option == "1"):
            print("Username: {}\nName: {}\nDirection: {}\n".format(user.worker_id,user.worker_name,user.worker_direction))
        elif (option == "2"):
            user.worker_name = input("Enter new name: ")
            user.worker_direction = input("Enter new direction: ")
            user.saveInstructor()
        elif (option == "3"):
            user.newSesion()
        elif(option == "4"):
            user.dropSesion()
        elif (option == "5"):
            user.newCategory(input("Enter the new category name: "))
        elif(option == "6"):
            print('''{} thanks for using our app'''.format(user.worker_name))
            user.logout()
            break
def enterNewUsername(cursor):
    while(True):
        try:
            username = input("Enter new username: ")
            cursor.execute('''select count(userid) from usuario where userid = '{}' '''.format(username))
            val = cursor.fetchone()
            cursor.execute('''select count(workerid
            ) from worker where workerid = '{}' '''.format(username))
            val2 = cursor.fetchone()
            if (val[0]!="0" and val[0]!=0 or val2[0]!="0" and val2[0]!=0):
                print("Enter another username")
            else:
                return username
        except:
            print("Couldn't be executed.")

def enterCardNumber():
    while(True):
        val = input("Enter the card number, must be 16 of length and full of digits: ")
        try:
            int(val)
            if (len(val)==16):
                return val
            else:
                print("It didn't have 16 numbers.")
        except:
            print("It didn't have full numbers.")
def enterPaymentMethod():
    while (True):
        select = input("Select between:\n1- Debit\n2- Credit\n")
        if (select == "1"):
            return "CREDIT"
        elif(select == "2"):
            return "DEBIT"
        else:
            print("The option selected is invalid, please try again.")
def enterSubscriptionType():
    while(True):
        select = input("Select between:\n1- Diamond subscription\n2- Gold subscription\n")
        if (select == "1"):
            return "DIAMOND"
        elif(select == "2"):
            return "GOLD"
        else:
            print("The option selected is invalid, please try again.")
def enterContractLenght():
    while(True):
        try:
            integer = int(input("Enter an the contract length in months: "))
            return integer
        except:
            print("The value entered was not correct")
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
def enterBirthdate():
    while (True):
        birthdate = input("Enter birthdate date (YYYY-MM-DD): ")
        birthdateAr = birthdate.split("-")
        try:
            datetime.datetime(int(birthdateAr[0]),int(birthdateAr[1]),int(birthdateAr[2]) )
            if (int(birthdateAr[0])>=1940):
                return birthdate
            print("Your sesion date doesn't make sense, nobody is that old please try again.\n\n")
        except:
            print("Incorrect data format, should be YYYY-MM-DD, please try again.\n\n")
def simulateOperations():
    cursor = connect()
    cursor.execute('''select current_date ''')
    current_date = cursor.fetchone()[0]
    cursor.execute('''select current_date + interval'6 month' ''')
    proxdate = cursor.fetchone()[0]
    cursor.execute('''select * from usuario''')
    usuarios = cursor.fetchall()
    admin = AdminCreateRole(getUser("postgres","Manager123"))
    try:
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
    except:
        pass
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
            for x in range(0,random.randint(0,10)):
                user.assignSesionRandom()
            if (random.randint(0,1)):
                user.direction = names.get_full_name()
                user.name = names.get_first_name()
                user.actualweight = random.randint(50,300)
                user.saveUser() 
                print('''
        The user {} change his profile'''.format(user.userid))
            user.updateSesionValuesRandom()
            cursor.execute('''select userid,avg(caloriesacomplished),avg(heartrate),sum(sesion.timelength)
            from sesionuser
            inner join sesion
            on sesionuser.sesioncode = sesion.sesioncode
            where sesion.sesiondate = '{}'  and userid = '{}'
            group by userid'''.format('2022-11-25',user.userid))
            values = cursor.fetchone()
            print('''
        The user {} burned {} calories in average and had a heart rate of {}, he trainned in {} min\n'''.format(user.userid,values[1],values[2],values[3].__str__()))
        except:
            pass
def randomBirthdate():
    start_date = datetime.date(1940, 1, 1)
    end_date = datetime.date(2013, 1, 1)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.__str__()
def randomDateSixMonth(cursor):
    cursor.execute('''select current_date+interval'6 month' ''')
    end_date = cursor.fetchone()[0]
    cursor.execute('''select current_date''')
    start_date = cursor.fetchone()[0]
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.__str__()
def randomDateHourTomorrow(cursor):
    cursor.execute('''select current_date+interval'1 day' ''')
    return [cursor.fetchone()[0].date().__str__(),datetime.time(random.randint(5,22),0,0).__str__(),datetime.time(0,random.randint(30,59),0).__str__()]
cursor = connect()
while (True):
    option = input("Welcome to the IHealth+ app, please select between:\n1- Log in\n2- Sign up\n3- Close app\n")
    if (option =="1"):
        username = input("Enter your username: ")
        password = maskpass.askpass(prompt="Enter password: ", mask="*")
        try:
            new_cursor = connectAdmin(username,password)
            values = getUser(username,password)
            if (values[len(values)-1]=="usuario"):
                user = User(values)
                user.getUserContract()
                userMenu(user)
            elif (values[len(values)-1]=="Instructor"):
                user = Instructor(values)
                user.getInstructorContract()
                instructorMenu(user)
            elif (values[len(values)-1] == "admin_reportery"):
                user = AdminReportery(values)
                reporteryMenu(user)
            elif (values[len(values)-1]=="admin_create_role"):
                user = AdminCreateRole(values)
                createRoleMenu(user)
            else:
                print("error")
        except:
            print("The username or the password entered is invalid")
    elif (option == "2"):
        values = getUser("postgres","Manager123")
        admin = AdminCreateRole(values)
        admin.createUser(enterNewUsername(admin.cursor),maskpass.askpass("Enter new password: ","*"),input("Enter name: "),enterBirthdate(),enterHeight(),enterWeight(),input("Enter direction: "),enterContractLenght(),enterSubscriptionType(),enterPaymentMethod(),enterCardNumber())
    elif (option == "3"):
        print("Thanks for using our app!\n")
        break
    else:
        print("The option enter is invalid, please try again.\n\n")

from ManagerFunctions import *
def loggedInUser(username, password, cursor):
    search = '''select * from usuario
    inner join(
        select * from usercontract
    ) as uc
    on uc.userid = usuario.userid
    where usuario.userid=\''''+username+'''\' and usuario.password =\''''+password+'''\' and uc.activeContract = True'''
    cursor.execute(search)
    value = cursor.fetchone()
    if (value!=None):
        user = searchUser(username, password, cursor)
        print("You have successfully logged in "+user[2]+".\n\n")
        checkUpdateInfo(user, cursor)
        while (True):
            option = input("\n\nSelect between this options:\n1- Search sesions\n2- Week calendar\n3- Statistics of any session\n4- Register weight\n5- Search old weight\n6- Cancel subscription\n7- Exit\n")
            if (option=="1"):
                searchSesions(user, cursor)
            elif (option == "2"):
                weekCalendar(user,cursor)
            elif (option == "3"):
                statisticSesion(user,cursor)
            elif (option == "4"):
                updateWeight(user,cursor)
            elif (option == "5"):
                searchOldWeight(user, cursor)
            elif (option == "6"):
                cancelSubscription(user,cursor)
            elif (option=="7"):
                break
            else:
                print("The entered option is invalid, try again.\n")
    else: print("You couldn't logged in, ask administration why.\n")
    return None
def searchSesions(user, cursor):
    while (True):
        option = input("Search sesions by:\n1- Sesion date\n2- Sesion hour\n3- Sesion length\n4- Sesion instructor name\n5- Sesion category\n6- Exit\n")
        query = '''select * from sesion where {} = \'{}\' and sesionstatus = \'wait\''''
        if (option == "1"):
            date = enterDate()
            cursor.execute(query.format("sesiondate",date))
            sesions = cursor.fetchall()
            if (len(sesions)!=0):
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
                        break
                    except:
                        print("The selected sesion is invalid, try again.\n")

                query2 = '''select count(sesionuser.sesioncode) from sesionuser
                inner join(
                    select * from sesion
                    where sesion.sesiondate = \'{}\' and
                    sesion.sesionhour = \'{}\' and sesion.timelength <= \'{}\'
                ) as s
                on s.sesioncode = sesionuser.sesioncode
                where userid = \'{}\' and sesionstatus = \'wait\''''
                cursor.execute(query2.format(sesion[2],sesion[3],sesion[4],user[0]))
                sesions = cursor.fetchone()[0]
                if (int(sesions)>0):
                    print("You can't assign to another sesion\n")
                else:
                    exercisetype = sesion[1]
                    cursor.execute('''insert into sesionuser(
                        userid,sesioncode,caloriesacomplished,heartrate,exercisetype,userweight
                    )
                    values(
                        \'{}\',{},0,0,\'{}\',{}
                    )'''.format(user[0],sesion[0],exercisetype,user[5]))
            else:
                print("There are no sesions that day.\n")
        elif (option == "2"):
            date = enterHour()
            cursor.execute(query.format("sesionhour",date))
            sesions = cursor.fetchall()
            if (len(sesions)!=0):
                value = 0
                print("Select between this: ")
                for x in sesions:
                    print(str(value)+"- Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Date: "+str(x[2])+" Description: "+str(x[6]))
                    value+=1
                sesion = ""
                while (True):
                    sesion = input("Enter sesion selected: ")
                    try:
                        sesion = sesions[int(sesion)]
                        break
                    except:
                        print("The selected sesion is invalid, try again.\n")

                query2 = '''select count(sesionuser.sesioncode) from sesionuser
                inner join(
                    select * from sesion
                    where sesion.sesiondate = \'{}\' and
                    sesion.sesionhour = \'{}\' and sesion.timelength <= \'{}\'
                ) as s
                on s.sesioncode = sesionuser.sesioncode
                where userid = \'{}\' and sesionstatus = \'wait\''''
                cursor.execute(query2.format(sesion[2],sesion[3],sesion[4],user[0]))
                sesions = cursor.fetchone()[0]
                if (int(sesions)>0):
                    print("You can't assign to another sesion\n")
                else:
                    exercisetype = sesion[1]
                    cursor.execute('''insert into sesionuser(
                        userid,sesioncode,caloriesacomplished,heartrate,exercisetype,userweight
                    )
                    values(
                        \'{}\',{},0,0,\'{}\',{}
                    )'''.format(user[0],sesion[0],exercisetype,user[5]))
            else:
                print("There are no sesions that hour.\n")
        elif (option =="3"):
            date = enterHour()
            cursor.execute(query.format("sesionlength",date))
            sesions = cursor.fetchall()
            if (len(sesions)!=0):
                value = 0
                print("Select between this: ")
                for x in sesions:
                    print(str(value)+"- Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Date: "+str(x[2])+" Description: "+str(x[6]))
                    value+=1
                sesion = ""
                while (True):
                    sesion = input("Enter sesion selected: ")
                    try:
                        sesion = sesions[int(sesion)]
                        break
                    except:
                        print("The selected sesion is invalid, try again.\n")

                query2 = '''select count(sesionuser.sesioncode) from sesionuser
                inner join(
                    select * from sesion
                    where sesion.sesiondate = \'{}\' and
                    sesion.sesionhour = \'{}\' and sesion.timelength <= \'{}\'
                ) as s
                on s.sesioncode = sesionuser.sesioncode
                where userid = \'{}\' and sesionstatus = \'wait\''''
                cursor.execute(query2.format(sesion[2],sesion[3],sesion[4],user[0]))
                sesions = cursor.fetchone()[0]
                if (int(sesions)>0):
                    print("You can't assign to another sesion\n")
                else:
                    exercisetype = sesion[1]
                    cursor.execute('''insert into sesionuser(
                        userid,sesioncode,caloriesacomplished,heartrate,exercisetype,userweight
                    )
                    values(
                        \'{}\',{},0,0,\'{}\',{}
                    )'''.format(user[0],sesion[0],exercisetype,user[5]))
            else:
                print("There are no sesions with that length.\n")
        elif (option == "4"):
            date = getInstructor2(cursor)
            cursor.execute('''select * from sesion where sesion.workerid = {}'''.format(date[0]))
            sesions = cursor.fetchall()
            if (len(sesions)!=0):
                value = 0
                print("Select between this: ")
                for x in sesions:
                    print(str(value)+"- Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Date: "+str(x[2])+" Description: "+str(x[6]))
                    value+=1
                sesion = ""
                while (True):
                    sesion = input("Enter sesion selected: ")
                    try:
                        sesion = sesions[int(sesion)]
                        break
                    except:
                        print("The selected sesion is invalid, try again.\n")

                query2 = '''select count(sesionuser.sesioncode) from sesionuser
                inner join(
                    select * from sesion
                    where sesion.sesiondate = \'{}\' and
                    sesion.sesionhour = \'{}\' and sesion.timelength <= \'{}\'
                ) as s
                on s.sesioncode = sesionuser.sesioncode
                where userid = \'{}\' and sesionstatus = \'wait\''''
                cursor.execute(query2.format(sesion[2],sesion[3],sesion[4],user[0]))
                sesions = cursor.fetchone()[0]
                if (int(sesions)>0):
                    print("You can't assign to another sesion\n")
                else:
                    exercisetype = sesion[1]
                    cursor.execute('''insert into sesionuser(
                        userid,sesioncode,caloriesacomplished,heartrate,exercisetype,userweight
                    )
                    values(
                        \'{}\',{},0,0,\'{}\',{}
                    )'''.format(user[0],sesion[0],exercisetype,user[5]))
            else:
                print("There are no sesions that hour.\n")
        elif (option == "5"):
            date = getCategory(cursor)
            cursor.execute(query.format("categorycode",date))
            sesions = cursor.fetchall()
            if (len(sesions)!=0):
                value = 0
                print("Select between this: ")
                for x in sesions:
                    print(str(value)+"- Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Date: "+str(x[2])+" Description: "+str(x[6]))
                    value+=1
                sesion = ""
                while (True):
                    sesion = input("Enter sesion selected: ")
                    try:
                        sesion = sesions[int(sesion)]
                        break
                    except:
                        print("The selected sesion is invalid, try again.\n")

                query2 = '''select count(sesionuser.sesioncode) from sesionuser
                inner join(
                    select * from sesion
                    where sesion.sesiondate = \'{}\' and
                    sesion.sesionhour = \'{}\' and sesion.timelength <= \'{}\'
                ) as s
                on s.sesioncode = sesionuser.sesioncode
                where userid = \'{}\' and sesionstatus = \'wait\''''
                cursor.execute(query2.format(sesion[2],sesion[3],sesion[4],user[0]))
                sesions = cursor.fetchone()[0]
                if (int(sesions)>0):
                    print("You can't assign to another sesion\n")
                else:
                    exercisetype = sesion[1]
                    cursor.execute('''insert into sesionuser(
                        userid,sesioncode,caloriesacomplished,heartrate,exercisetype,userweight
                    )
                    values(
                        \'{}\',{},0,0,\'{}\',{}
                    )'''.format(user[0],sesion[0],exercisetype,user[5]))
            else:
                print("There are no sesions that hour.\n")
        elif (option == "6"):
            break   
def getInstructor2(cursor):
    cursor.execute('''select * from worker where workertype = 'Instr' ''')
    instructors = cursor.fetchall()
    for x in instructors:
        print("Instructor name: "+x[2])
    while (True):
        id = input("Enter the instructor name: ")
        try:
            cursor.execute('''select * from worker where workername = \'{}\' and workertype = \'Instr\''''.format(id))  
            instructor = cursor.fetchone()
            if (instructor != None):return instructor
            int(instructor)
        except:
            print("The instructor name entered is invalid.\n")
def weekCalendar(user, cursor):
    print("We need the initial date.\n")
    initdate = enterDate()
    print("We need the last date.\n")
    lastdate = enterDate()
    cursor.execute('''select * from sesionuser inner join (select sesioncode,sesiondate, sesionhour,sesionstatus from sesion where sesion.sesiondate <= \'{}\' and sesion.sesiondate >= \'{}\') as s on s.sesioncode = sesionuser.sesioncode where sesionuser.userid = \'{}\''''.format(lastdate, initdate, user[0]))
    sesions = cursor.fetchall()
    id = initdate = initdate.split("-")
    ld = lastdate = lastdate.split("-")
    id[0]=int(id[0])
    id[1]=int(id[1])
    id[2]=int(id[2])
    initdate = datetime.datetime(int(initdate[0]),int(initdate[1]),int(initdate[2]))
    lastdate = datetime.datetime(int(lastdate[0]),int(lastdate[1]),int(lastdate[2]))
    difference = int((lastdate - initdate).days)*24
    for x in range(int((lastdate - initdate).days)):
        id[2]=int(id[2])+1
        if (id[2]==31 and (id[1]==4 or id[1]==6 or id[1]==9 or id[1]==11)):
            id[2]=1
            id[1]=int(id[1])+1
        elif (id[2]==32 and (id[1]==1 or id[1]==3 or id[1]==5 or id[1]==7 or id[1]==8 or id[1]==10)):
            id[2]=1
            id[1]=int(id[1])+1
        if (id[1]==12 and id[2]==31):
            id[0]=int(id[0])+1
            id[1]=1
        date = str(id[0])+"-"
        if (id[1]<10):
            date+="0"+str(id[1])+"-"
        else:
            date+=str(id[1])+"-"
        if (id[2]<10):
            date+="0"+str(id[2])
        else:
            date+=str(id[2])
        print("Date : {} ".format(date))
        for y in range(24):
            hour = ""
            if (y<10):
                hour = "0"+str(y)+":00:00"
            else:
                hour = str(y)+":00:00"
            timei = datetime.time(y,0)
            dat = datetime.date(id[0],id[1],id[2])
            timef = datetime.time(y,59)
            printing = ""
            prin = True
            for z in sesions:
                if(timei<=z[8]<=timef and dat==z[7]):
                    printing = (hour+"- Exercise type: "+z[4])
                    print(printing)
                else:
                    printing = (hour+"- None")
                    prin = True
            if (prin):
                print(printing)
            

def cancelSubscription(user,cursor):
    cursor.execute('''select max(contractcode) from usercontract where userid = \'{}\''''.format(user[0]))
    getcontractcode = str(cursor.fetchone()[0])
    query = '''update usercontract set activecontract = False where contractcode = {}'''.format(getcontractcode)
    cursor.execute(query)
def searchOldWeight(user, cursor):
    cursor.execute('''select * from sesion inner join (select * from sesionuser where userid = \'{}\') as us on us.sesioncode = sesion.sesioncode'''.format(user[0]))
    sesions = cursor.fetchall()
    print("Select between this: ")
    value = 0
    for x in sesions:
        print(str(value)+"- Sesion date: "+str(x[2])+" Weight: "+str(x[14]))
        value+=1
def updateWeight(user, cursor):
    newWeight = enterWeight()
    cursor.execute('''update usuario set actualweight = {} where userid = \'{}\''''.format(newWeight, user[0]))
def statisticSesion(user, cursor):
    cursor.execute('''select * from sesion inner join (select * from sesionuser where userid = \'{}\') as us on us.sesioncode = sesion.sesioncode'''.format(user[0]))
    sesions = cursor.fetchall()
    print("Select between this: ")
    value = 0
    for x in sesions:
        print(str(value)+"- Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Hour: "+str(x[3])+" Description: "+str(x[6]))
        value+=1
    sesion = ""
    while (True):
        sesion = input("Enter sesion selected: ")
        try:
            sesion = sesions[int(sesion)]
            break
        except:
            print("The selected sesion is invalid, try again.\n")
    cursor.execute('''select * from sesion inner join (select * from sesionuser where userid = \'{}\') as us on us.sesioncode = sesion.sesioncode where sesion.sesioncode = {}'''.format(user[0],sesion[0]))
    print("Sesion code: "+str(x[0])+" Name: "+str(x[1])+" Hour: "+str(x[3])+" Description: "+str(x[6])+" Exercise type: "+str(x[13])+ " Calories: "+str(x[11])+" Hear rate: "+str(x[12]))
def enterSomething(something):
    while (True):
        calories = input("Enter the amount of {}: ".format(something))
        try:
            float(calories)
            return calories
        except: print("The amount of {} entered is invalid.\n".format(something))
def checkUpdateInfo(user, cursor):
    print("This will take you a few minutes, we need to update info of some sesions that you have already been.\n")
    cursor.execute('''select * from sesionuser inner join (select sesioncode, sesiondate, sesionhour from sesion where sesion.sesionstatus = 'done') as s on s.sesioncode = sesionuser.sesioncode where sesionuser.userid = \'{}\' and sesionuser.caloriesacomplished = 0.0'''.format(user[0]))
    sesions = cursor.fetchall()
    for x in sesions:
        print("This is the sesion made in {} at {} hrs, it was named {}.\n".format(x[7],x[8],x[4]))
        calories = enterSomething("calories")
        heartrate = enterSomething("heart rate")
        cursor.execute('''update sesionuser set caloriesacomplished = {}, heartrate = {} where sesionuser.sesioncode = {}'''.format(calories, heartrate, x[1]))
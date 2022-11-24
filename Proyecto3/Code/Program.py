import maskpass
from Connection.ConectDB import *
from ManagerFunctions import *
from InstructorFunctions import *
from UserFunctions import *
def loggingIn(username, password, cursor):
    if (searchUser(username=username, password=password, cursor=cursor)!=None):
        loggedInUser(username=username, password=password, cursor=cursor)
    elif (searchInstructor(username=username, password=password, cursor=cursor)!=None):
        loggedInstructor(username=username, password=password, cursor=cursor)
    elif (searchAdmin(username=username, password=password, cursor=cursor)!=None):
        loggedInAdmin(username=username, password=password, cursor=cursor)
    else:
        print("The username or password given aren't correct.\n")

cursor = connectDB()
while (True):
    option = input("Welcome to the IHealth+ app, please select between:\n1- Log in\n2- Sign up\n3- Close app\n")
    if (option =="1"):
        username = input("Enter your username: ")
        password = maskpass.askpass(prompt="Enter password: ", mask="*")
        loggingIn(username=username, password=password, cursor=cursor)
    elif (option == "2"):
        createUser(cursor=cursor)
    elif (option == "3"):
        print("Thanks for using our app!\n")
        break
    else:
        print("The option enter is invalid, please try again.\n\n")

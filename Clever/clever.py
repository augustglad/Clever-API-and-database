#Authors: Group 1 international
#Date 11.04.22
#This script is an API that connects to a the database called DUPA2
# it does so by using the module mysql.
import mysql.connector

#Enter the host, user, password and database that is listed for your connection in mysql
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "vfp59fdp",
    database = "DUPA2"
)


mycursor = mydb.cursor()

#This is a function that interracts with the database and it adds 1 to the USED Column with the according ID
def carconnects(ID):
    #Getting the current amount of USED chargers in the database
    mycursor.execute('SELECT USED FROM CHARGER WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    carsconnected = myresult[0]
    #Getting the total amount of outlets from the OUTLETCOUNT in the database
    mycursor.execute('SELECT OUTLETCOUNT FROM CHARGER WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    outletcount = myresult[0]
    #If carsconnected/USED value is smaller than the OUTLETCOUNT, then it adds one to carsconnected.
    if carsconnected < outletcount:
        carsconnected = carsconnected + 1
        #Updating the USED value to the new carsconnected value to the according ID value
        sql = 'UPDATE CHARGER SET USED = %s WHERE ID = %s' % (carsconnected, ID)
        mycursor.execute(sql)
        mydb.commit()
        print("""
        Car connected succesfully

        """)
    #if carsconnected are smaller or equal to the outletcount, i.e no more outlets are available, give an error
    if carsconnected >= outletcount:
        print('no more slots available')
    ID = 0

#this is a function that interracts with the database and does the opposite of the carconnects function, it removes 1 from the carsconnected
def cardisconnects(ID):
    mycursor.execute('SELECT USED FROM CHARGER WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    carsconnected = myresult[0]
    mycursor.execute('SELECT OUTLETCOUNT FROM CHARGER WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    outletcount = myresult[0]
    if carsconnected <= outletcount and carsconnected != 0:
        carsconnected = carsconnected -1
        sql = 'UPDATE CHARGER SET USED = %s WHERE ID = %s' % (carsconnected, ID)
        mycursor.execute(sql)
        mydb.commit()
        print("""
        Car succesfully disconnected

        """)

    else:
        print("""
        No cars are connected

        """)
    ID = 0

#This is a function that takes data from the database and shows the user how many chargers are available at the chosen station
def chargeravailable(ID):
    #extract OUTLETCOUNT value from database
    mycursor.execute('SELECT OUTLETCOUNT FROM CHARGER WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    #set the OUTLETCOUNT value to outlets
    outlets = myresult[0]
    #Extract the USED value from database from given ID
    mycursor.execute('SELECT USED FROM CHARGER WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    #set the USED value to outlets_used
    outlets_used = myresult[0]
    #if statement to print the amount of chargers available
    if outlets >= outlets_used:
        print('\n', outlets - outlets_used, '/', outlets, ' chargers are available \n \n')
    else:
        print('\n', outlets - outlets_used, '/', outlets, 'chargers are available \n \n')
    ID = 0

#Function that shows the busyness of a station based on the busyness value given in the database
#busyness value is rated from 1 till 3 where 3 is very busy and 1 is not busy
def showbusyness(ID):
    #extract the busyvalue of the given ID
    mycursor.execute('SELECT BUSYVALUE FROM STATION WHERE ID = %s;' % ID)
    myresult = mycursor.fetchone()
    #giving myresult the BUSYVALUE
    myresult = myresult[0]
    if myresult == 1:
        print('\n Station number %s is usually not busy at this moment \n \n' % ID)
    if myresult == 2:
        print(' \n Station number %s is usually moderately busy at this moment \n \n' % ID)
    if myresult == 3:
        print('\n Station number %s is usually very busy at this moment \n \n' % ID)
    #if no busyvalue is given, print that no data is available
    else:
        '\n No data available on the usual busyness level of this station \n \n'
    ID = 0
#The menu function
def menu():
    print('Please choose which charging station you would like information on')
    #displays all ID with their ADRESS value from the STATION TABLE
    mycursor.execute("SELECT ID, ADRESS FROM STATION")
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


    #if input is not an integer, try again
    try:
        ID = int(input('>'))
    except ValueError:
        print('That is not a valid charger, try again')
        ID = int(input('>'))


    print("""What would you like to do:
    1: See busyness rate of the station
    2: See how many chargers are available
    3: Connect your car
    4: Disconnect your car """)
    action = 0
    while action == 0:
        try:
            action = int(input('>'))
        except ValueError:
            print('That is not a valid action, try again')
        #do the function based on what input was given
        if action == 1:
            showbusyness(ID)
        if action == 2:
            print(ID)
            chargeravailable(ID)
        if action == 3:
            carconnects(ID)
        if action == 4:
            cardisconnects(ID)
ID = 0
while ID == 0:
    menu()

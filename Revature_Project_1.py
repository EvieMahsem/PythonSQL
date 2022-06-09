import mysql.connector


# This is a class for the C of the CRUD operations
# class Creation():
#     def __init__(self, connection, database_name, table_name):
#         self.database_name = database_name
#         self.table_name = table_name

def create_database(connection, databsae_name):
    databaseObject = connection.cursor()
    databaseObject.execute(f"CREATE DATABASE {databsae_name};")

def use_database(connection, databsae_name):
    useObject = connection.cursor()
    useObject.execute(f"USE {databsae_name};")

# This is a class for the R of the CRUD operations
# class Sql_Read():


# This is a class for the U of the CRUD operations
# class Sql_Update():


# This is a class for the D of the CRUD operations
# class Sql_Delete():




###This is used to run the code. This will be later moved to a run sutie.###


def setup():
    # User inputted MySQL server info
    username = input("Input you MySql username: ")
    host = input("Input you MySql hostname: ")
    port = input("What is your MySQL port: ")
    passwd1 = input("Password for your connection: ")
    #Connecting to the server
    global conn
    conn = mysql.connector.connect(user = username,
                                host = host,
                                port = port,
                                passwd = passwd1)

    databases = []
    while True:
        print("Do you want to create a yes or no?")
        DBCreation = input("\t Type 1 for yes\n \t Type 2 for no: ")
        if int(DBCreation) == 1:
            name = input("Name your database please: ")
            databases.append(name)
            create_database(conn, name)
        elif int(DBCreation) == 2:
            print("Which database do you want to use: ", databases)
            name = input("The database you want: ")
            use_database(conn, name)
            break

setup()


def shutdown():
    conn.close()
shutdown()
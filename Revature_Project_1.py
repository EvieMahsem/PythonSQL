import maskpass
import mysql.connector

def setup():
    # User inputted MySQL server info
    username = input("Input your MySql username: ")
    host = input("Input your MySql hostname: ")
    port = input("What is your MySQL port: ")
    passwd1 = maskpass.askpass(prompt="What is your MySQL password: ", mask="*")

    #Connecting to the server
    global conn
    conn = mysql.connector.connect(user = username,
                                host = host,
                                port = port,
                                passwd = passwd1)

    #Database selection / creation                            
    while True:
        print("Do you want to create database a yes or no?")
        DBCreation = input("\t Type yes or no: ")

        if DBCreation.lower() == "yes":

            #Text prompts and writes a file with created databases
            name = input("Name your database please: ")
            databases = open("databases.txt", "a")
            databases.write(name + ",")
            databases.close()

            #Creates the database
            databaseObject = conn.cursor()
            databaseObject.execute(f"CREATE DATABASE {name};")
        elif DBCreation.lower() == "no":

            #Text prompts and reads the created databases
            print("Which database do you want to use: ")
            databases = open("databases.txt", "r")
            print("Created databases:", databases.read())
            databases.close()
            name = input("The database you want: ")

            #Uses the database selected
            useObject = conn.cursor()
            useObject.execute(f"USE {name};")
            
            #Stops the while loop
            break

def table_creation():
    while True:
        yes_no = input("Are you wanting to create a table(yes/no): ")
        if yes_no.lower() == "yes":
            #Text prompts and writes a file with created tables
            table_name = input("Name your table please: ")
            tables = open("tables.txt", "a")
            tables.write(table_name + ",")
            tables.close()

            #Text prompt for what type of table to make
            p_f_d = input("What type of key do you want?\n \t 1. Primary Key\n \t 2. Foreign Key\n \t 3. No Key (default) \n \t Response: ")
            num_of_col = input("How many columns do you want: ")

            if int(p_f_d) == 1:

                #Takes how many columns you want and will let you insert column_name and datatype pairs and then formats it into a 1 string
                col_datatype = []
                for i in range(int(num_of_col)):
                    x = input("What is column name and datatype (column_name datatype)?\nLink to datatypes: https://www.w3schools.com/mysql/mysql_datatypes.asp \n \t Your input please: ")
                    col_datatype.append(x)
                string_of_col = ",".join(col_datatype)

                #Tells you the current columns and asks for which column should have the primary key
                print("The tables current columns: ", string_of_col)
                key = input("Which column should be the primary key: ")

                #Runs the SQL code
                tableObject = conn.cursor()
                tableObject.execute(f"CREATE TABLE {table_name} ({string_of_col}, PRIMARY KEY ({key}));")

            elif int(p_f_d) == 2:

                #Takes how many columns you want and will let you insert column_name and datatype pairs and then formats it into a 1 string
                col_datatype = []
                for i in range(int(num_of_col)):
                    x = input("What is column name and datatype (column_name datatype)?\nLink to datatypes: https://www.w3schools.com/mysql/mysql_datatypes.asp \n \t Your input please: ")
                    col_datatype.append(x)
                string_of_col = ",".join(col_datatype)

                #Tells you the current columns
                print("The tables current columns: ", string_of_col)

                #Gives the made tables, so you can select which one you want for the foreign key
                current_table = open("tables.txt", "r")
                print("Created tables: ", current_table.read())
                current_table.close()

                #Gets the reference table and comlumn
                key_table = input("Which table does the foreign key reference: ")
                key = input("Which column should the foreign key reference: ")

                #Runs the SQL code
                tableObject = conn.cursor()
                tableObject.execute(f"CREATE TABLE {table_name} ({string_of_col}, FOREIGN KEY ({key}) REFERENCES {key_table}({key}));")
            else:
                #Takes how many columns you want and will let you insert column_name and datatype pairs and then formats it into a 1 string
                col_datatype = []
                for i in range(int(num_of_col)):
                    x = input("What is column name and datatype (column_name datatype)?\nLink to datatypes: https://www.w3schools.com/mysql/mysql_datatypes.asp \n \t Your input please: ")
                    col_datatype.append(x)
                string_of_col = ",".join(col_datatype)

                #Tells you the current columns
                print("The tables current columns: ", string_of_col)

                #Runs the SQL code
                tableObject = conn.cursor()
                tableObject.execute(f"CREATE TABLE {table_name} ({string_of_col});")

        else:
            break



def shutdown():
    conn.close()


#Runs all of the functions (Will be turning this into a menu)
setup()
table_creation()

shutdown()



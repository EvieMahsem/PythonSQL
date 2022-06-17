import maskpass
import mysql.connector
import names
import random
from pyparsing import col
from tabulate import tabulate

def delete_from_text(file, input):
    with open(f"{file}", "r") as f:
        lines = f.readlines()
    with open(f"{file}", "w") as f:
        for line in lines:
            if line.strip("\n") != f"{input}":
                f.write(line)    

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

def database_creation():
    #Database creation                            
    while True:
        #Text prompts with the name of your database
        name = input("Name your database please: ")

        #Creates the database
        try:
            databaseObject = conn.cursor()
            databaseObject.execute(f"CREATE DATABASE {name};")
        except:
            print("Please input a name that does not already exist")
        else:
            #If there is no error, it writes the name of the database to the txt file
            databases = open("databases.txt", "a")
            databases.write(name + "\n")
            databases.close()

        break

def database_selection():
    #Text prompts and reads the created databases
    print("Which database do you want to use: ")
    databases = open("databases.txt", "r")
    print("Created databases:\n" + databases.read())
    databases.close()
    name = input("The database you want: ")
    global database_selected
    database_selected = name

    #Uses the database selected
    try:
        useObject = conn.cursor()
        useObject.execute(f"USE {name};")
    except:
        print("Please select a database that exists.")

def table_creation():
    while True:
        #Text prompts and writes a file with created tables
        table_name = input("Name your table please: ")

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
            try:
                tableObject = conn.cursor()
                tableObject.execute(f"CREATE TABLE {table_name} ({string_of_col}, PRIMARY KEY ({key}));")
            except:
                print("Most likly an SQL error, so make sure you typed everything in correctly")
            else:
                tables_col = open("tables.txt", "a")
                tables_col.write(table_name + f":{database_selected}:PK:" + string_of_col + "\n")
                tables_col.close()

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
            print("Created tables:\n " + current_table.read())
            current_table.close()

            #Gets the reference table and comlumn
            key_table = input("Which table does the foreign key reference: ")
            key = input("Which column should the foreign key reference: ")



            #Runs the SQL code
            try:
                tableObject = conn.cursor()
                tableObject.execute(f"CREATE TABLE {table_name} ({string_of_col}, FOREIGN KEY ({key}) REFERENCES {key_table}({key}));")
            except:
                print("Most likly an SQL error, so make sure you typed everything in correctly")
            else:  
                tables_col = open("tables.txt", "a")
                tables_col.write(table_name + f":{database_selected}:FK({key}):" + string_of_col + "\n")
                tables_col.close()


        elif int(p_f_d) == 3:
            #Takes how many columns you want and will let you insert column_name and datatype pairs and then formats it into a 1 string
            col_datatype = []
            for i in range(int(num_of_col)):
                x = input("What is column name and datatype (column_name datatype)?\nLink to datatypes: https://www.w3schools.com/mysql/mysql_datatypes.asp \n \t Your input please: ")
                col_datatype.append(x)
            string_of_col = ",".join(col_datatype)

            #Tells you the current columns
            print("The tables current columns: ", string_of_col)

            #Runs the SQL code
            try:
                tableObject = conn.cursor()
                tableObject.execute(f"CREATE TABLE {table_name} ({string_of_col});")
            except:
                print("Most likly an SQL error, so make sure you typed everything in correctly")
            else:
                tables_col = open("tables.txt", "a")
                tables_col.write(table_name + f":{database_selected}:NO_Key:" + string_of_col + "\n")
                tables_col.close()       
        else:
            print("Please insert a vaild value.")
        break

def table_insertion():
    while True:
        question = input("""Welcome to data insertion:
    1. Insert data
    2. Insert data with random values (Hard Coded, so not good for outside this project)
    3. Exit
    Enter a Number: """)
        if int(question) == 1:

            print("Warning: You must input data into a primary key table, before you can insert into a foreign key table!!!!\n")
            #Shows the current tables
            tables = open("tables.txt", "r")
            print("Created Tables (table_name:database:KeyType:Column_Name DataType, ...):\n" + tables.read())
            tables.close()
            #Gets the columns and table name
            table_name = input("What table do you want to insert into: ")
            coln = input("What are the column you would like to input (column1, column2, column3,...): ")


            num_of_row = input("How many rows do you want to input: ")
            x = 0
            while x < int(num_of_row):
                x += 1
                values = input("What are the values you would like to input (val1, 'val2', 'val3',...): ")

                #Runs the SQL code
                try:
                    insertObject = conn.cursor()
                    insertObject.execute(f"INSERT INTO {table_name} ({coln}) VALUES ({values});")
                    conn.commit()
                except:
                    print("Most likly an SQL error, so make sure you typed everything in correctly")
                    break

        elif int(question) == 2:
            #Hard coded data for random
            states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI","MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC","ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD","TN","TX","UT","VT","WA", "WV", "WI", "WY"]
            clothing = ['T-Shirt', "Jeans", "Khakis", 'Blouse', "Vest", "Socks", "Gym Shorts"]
            colors = ['red', 'blue', 'grey', 'white', 'black', 'tan', 'green', 'pink']
            online_or_instore = ["Bought in Store", "Bought Online"] 
            print("Warning: You must input data into a primary key table, before you can insert into a foreign key table!!!!\n")

            #Shows the current tables
            tables = open("tables.txt", "r")
            print("Created Tables (table_name:database:KeyType:Column_Name DataType, ...):\n" + tables.read())
            tables.close()

            #Gets the columns and table name and total rows
            table_name = input("What table do you want to insert into: ")
            coln = input("What are the column you would like to input (column1, column2, column3,...): ")
            num_of_row = input("How many rows do you want to input: ")


            #Inserts random data
            x = 0
            while x < int(num_of_row):
                x += 1
                #values = [str(x), f'"{names.get_first_name()}"',f'"{names.get_last_name()}"', f'"{random.choice(states)}"']
                # values = [str(x), f'"{random.choice(clothing)}"',f'"{random.choice(colors)}"']
                values = [str(x), f'"{random.choice(online_or_instore)}"']

                val = ','.join(values)
                print(val)
                #Runs the SQL code
                insertObject = conn.cursor()
                insertObject.execute(f"INSERT INTO {table_name} ({coln}) VALUES ({val});")
                conn.commit()    


        elif int(question) == 3:
            break        
        else:
            print("Please input a vaild value.")


def data_update():
    x = input("How many changes do you want to make (number): ")
    y = 0
    while y < int(x):
        y += 1
        tables = open("tables.txt", "r")
        print("From the following created Tables in the format (table_name:database:KeyType:Column_Name DataType, ...):\n" + tables.read())
        tables.close()
        table_to_update = input("Which table do you want to update? ")
        column_changing = input("Which column are you looking to change a value in? ")
        new_val = input("What is the new value you would like to enter? ")
        column_identifier = input("Which column is the Primary Key or you want to use as an column identifier? ")
        value_identifier = input("What is the value you are using as an value identifier? ")
        
        try:
            updateObject = conn.cursor()
            updateObject.execute(f"UPDATE {table_to_update} SET {column_changing} = {new_val} WHERE {column_identifier} = {value_identifier};")
            conn.commit()
        except:
            print("Most likly an SQL error, so make sure you typed everything in correctly")
            break

def delete_data():
    while True:
        print(""" What would you like to do?
    1. Remove the whole table
    2. Remove the data from the table
    3. Remove the whole database
    4. Exit
        """)
        x = input("Please select one: ")
        if int(x) == 1:
            tables = open("tables.txt", "r")
            print("Which table do you want to remove. The Created tables (table_name:database:KeyType:Column_Name DataType, ...):\n" + tables.read())
            tables.close()

            table_to_del = input("Input the table_name that you want to delete:\n ")

            try:
                dropObject = conn.cursor()
                dropObject.execute(f"DROP TABLE {table_to_del};")
                
                path_to_del = input("\nInput the full path to del i.e(table_name:database:KeyType:Column_Name DataType, ...): ")
                delete_from_text("tables.txt", path_to_del)
            except:
                print("Most likly an SQL error, so make sure you typed everything in correctly")

        elif int(x)==2:
            
            print("Which table do you want to remove data from:\n ")
            tables = open("tables.txt", "r")
            print("Created tables (table_name:database:KeyType:Column_Name DataType, ...):\n" + tables.read())
            tables.close()

            data_to_del = input("\nInput the table_name that you want to truncate: ")

            try:
                truncateObject = conn.cursor()
                truncateObject.execute(f"TRUNCATE TABLE {data_to_del};")
            except:
                print("Most likly an SQL error, so make sure you typed everything in correctly")                

        elif int(x) == 3:

            print("Which database do you want to remove:\n ")
            databases = open("databases.txt", "r")
            print("Created databases:\n" + databases.read())
            databases.close()

            try:
                database_to_del = input("Input the database name: ")
                dropObject = conn.cursor()
                dropObject.execute(f"DROP DATABASE {database_to_del};")

                delete_from_text("databases.txt", database_to_del)
            except:
                print("Most likly an SQL error, so make sure you typed everything in correctly")

        elif int(x) == 4:
            break
        else:
            print("Please input a valid number.")

def show_tables():
    print("Hello, which table do you want to show?")
    tables = open("tables.txt", "r")
    print("Created Tables in the format (table_name:database:KeyType:Column_Name DataType, ...):\n" + tables.read())
    tables.close()

    x = input("Please input the table_name you want to see: ")
    y = input("Please, input the columns you want to see in coln1, coln2, ... format otherwise to see all use *: ")

    try:
        showObject = conn.cursor()
        showObject.execute(f"SELECT {y} FROM {x};")
        query_result = showObject.fetchall()
        print(tabulate(query_result))
    except:
        print("Make sure you typed everything in correctly and are in the right database!")


def shutdown():
    conn.close()
    
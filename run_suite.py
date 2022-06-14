from Revature_Project_1 import *

print("Thank you from using Evie's DataBase Mangament System for all of your store's needs!")
while True:
    print("""
    \nWhat would you like to do?
    \t1. Setup (Required)
    \t2. Databases Creation
    \t3. Databases Selection (Required)
    \t4. Table Creation
    \t5. Insert Data (Somewhat Implemented)
    \t6. Update Data
    \t7. Delete Tables/Databases
    \t8. Show Tables
    \t9. Shutdown
    """)
    x = input("What is your selection: ")
    if int(x) == 1:
        setup()
    elif int(x) == 2:
        database_creation()
    elif int(x) == 3:
        database_selection()
    elif int(x) == 4:
        table_creation()
    elif int(x) == 5:
        table_insertion()
    elif int(x) == 6:
        data_update()
    elif int(x) == 7:
        delete_data()
    elif int(x) == 8:
        show_tables()
    elif int(x) == 9:
        shutdown()
        break
    else:
        print(f"The value {x} is not a vaild input.\n")

from Revature_Project_1 import *

print("Thank you from using Evie's Database Mangament System for all of your store's needs!")
while True:
    print("What would you like to do?")
    print("\t1. Setup (Required)")
    print("\t2. Databases Creation and Selection")
    print("\t3. Table Creation")
    print("\t4. Insert Data (Not Implemented)")
    print("\t5. Alter Data (Not Implemented)")
    print("\t6. Delete Tables/Databases (Not Implemented)")
    print("\t7. Show Tables (Not Implemented)")
    print("\t8. Shutdown")
    
    x = input("What is your selection: ")

    if int(x) == 1:
        setup()
    elif int(x) == 2:
        database_selection_creation()
    elif int(x) == 3:
        table_creation()
    elif int(x) == 4:
        table_insertion()
    elif int(x) == 5:
        table_alteration()
    elif int(x) == 6:
        delete_data()
    elif int(x) == 7:
        show_tables()
    elif int(x) == 8:
        shutdown()
        break
        
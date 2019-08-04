import mysql.connector

class Tinder:
    
    def __init__(self):
        
        self.conn = mysql.connector.connect(host="localhost",user="root",password="",database="tinderb1")
        self.mycursor = self.conn.cursor()
        self.program_menu()

    def program_menu(self):
        
        program_input = input("""\n        Hi! Welcome to Tinder :
        1. Enter 1 to login.
        2. Enter 2 to register.
        3. Enter Anything else to exit : """)
        
        if program_input == '1':
            self.login()
        elif program_input == '2':
            self.register()
        else:
            print("Bye")

    def register(self):
        
        print("\nWelcome to the registration page : \n")
        
        name = input("Enter Name : ")
        email = input("Enter email : ")
        password = input("Enter password : ")
        gender = input("Enter gender : ")
        age = int(input("Enter age : "))
        city = input("Enter city : ")

        self.mycursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        
        user_list1 = self.mycursor.fetchall()

        if len(user_list1) > 0:
            print("\nEmail already exists.")
            self.program_menu()

        else:
            self.mycursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `Gender`, `Age`, `City`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}')""".format(name,email,password,gender,age,city))
            self.conn.commit()
            print("Registration Successful")
            self.program_menu()

    def login(self):
        
        email = input("Enter email : ")
        password = input("Enter password : ")
        
        self.mycursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        
        user_list1 = self.mycursor.fetchall()
        
        self.mycursor.execute("""SELECT * FROM `users` WHERE `password` LIKE '{}'""".format(password))
        
        user_list2 = self.mycursor.fetchall()

        if len(user_list1) > 0 and len(user_list2) > 0:
            print("\nWelcome")
            self.current_user_id = user_list1[0][0]
            self.user_menu()
        elif len(user_list1) > 0 and len(user_list2) == 0:
            print("\nIncorrect password")
            self.program_menu()
        elif len(user_list1) == 0 and len(user_list2) > 0:
            print("\nIncorrect email")
            self.program_menu()
        else:
            print("\nIncorrect email and password")
            self.program_menu()

    def user_menu(self):

        user_input = input("""\n        Hi!, How would you like to proceed?
        1. View all users.
        2. View who proposed you.
        3. View your proposals.
        4. View your matches.
        5. Anything else to logout.
        """)
        
        if user_input == '1':
            self.view_all_users()
        elif user_input == '2':
            self.view_proposed()
        elif user_input == '3':
            self.view_proposals()
        elif user_input == '4':
            self.view_matches()
        else:
            self.logout()

    def view_all_users(self):

        self.mycursor.execute("""SELECT * FROM `users` WHERE `user_id` NOT LIKE '{}'""".format(self.current_user_id))
        all_users = self.mycursor.fetchall()
        
        print("USER ID  \t|\tNAME  \t \t|\tGENDER  \t|\tAGE  \t|\tCITY\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        
        for i in all_users:
            print("\t",i[0],"\t|\t",i[1],"\t|\t",i[4],"\t\t|\t",i[5],"\t|\t",i[6],"\n","-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            
        option = input("\nEnter 'yes' to propose someone or anything else to return to menu : ")
        
        if option == "yes":
            self.juliet_id=int(input("\nEnter the id of the User whom you want to propose : "))
            self.propose(self.juliet_id)
        else:
            self.user_menu()

    def propose(self,juliet_id):
        
        self.mycursor.execute("""INSERT INTO `proposals` (`proposal_id`, `romeo_id`, `juliet_id`) VALUES (NULL, '{}', '{}')""".format(self.current_user_id,juliet_id))
        self.conn.commit()
        
        print("\nProposal Successful")
        self.user_menu()

    def view_proposed(self):
        
        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN `users` u ON u.`user_id`=p.`romeo_id` WHERE p.`juliet_id`= '{}' """.format(self.current_user_id))
        who_proposed = self.mycursor.fetchall()
        
        print("NAME  \t \t|\tEMAIL ID  \t|\tGENDER  \t|\tAGE  \t|\tCITY\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        
        for i in who_proposed:
            print(i[4],"\t|\t",i[5],"\t|\t",i[7],"\t\t|\t",i[8],"\t|\t",i[9],"\n","-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        self.user_menu()

    def view_proposals(self):

        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN `users` u ON u.`user_id`=p.`juliet_id` WHERE p.`romeo_id`= '{}' """.format(self.current_user_id))
        who_i_proposed = self.mycursor.fetchall()

        print("NAME  \t \t|\tEMAIL ID  \t|\tGENDER  \t|\tAGE  \t|\tCITY\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        for i in who_i_proposed:
            print(i[4],"\t|\t",i[5],"\t|\t",i[7],"\t\t|\t",i[8],"\t|\t",i[9],"\n","-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        self.user_menu()

    def view_matches(self):

        self.mycursor.execute("""SELECT * FROM `proposals` p
                                             JOIN `users` u ON u.`user_id`=p.`juliet_id`
                                             WHERE p.`juliet_id` IN (SELECT `romeo_id` FROM `proposals` WHERE `juliet_id` LIKE '{}')
                                             AND p.`romeo_id` LIKE '{}'""".format(self.current_user_id,self.current_user_id))
        matched = self.mycursor.fetchall()

        if len(matched) > 0:
            print("NAME  \t \t|\tEMAIL ID  \t|\tGENDER  \t|\tAGE  \t|\tCITY\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for i in matched:
                print(i[4],"\t|\t",i[5],"\t|\t",i[7],"\t\t|\t",i[8],"\t|\t",i[9],"\n","-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        else:
            print("Sorry! No one is matched with you yet.... But don't lose hope :)")

        self.user_menu()

    def logout(self):

        self.current_user_id=0
        option = input("\nDo you really want to logout and return to login page? \nEnter 'yes' to logout , anything else to stay on this page : ")

        if option == "yes":
            print("Logged Out...")
            self.program_menu()
        else:
            self.user_menu()

obj1 = Tinder()

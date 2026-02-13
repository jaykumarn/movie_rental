from domain.Rental import Rental
from domain.Errors import DuplicateException, InexistingException,\
    AlreadyBurrowed
from datetime import datetime, timedelta

class UI():
    def __init__(self, ctrl):
        self.__ctrl = ctrl
        
    def menu(self):
        menu_list = ""
        menu_list += "\t\tMOVIE RENTAL SHOP MANAGEMENT \n\n"
        menu_list += "\t\t\t  Menu:\n\n"
        menu_list += "\t To get all rentals type <list rentals>. \n"
        menu_list += "\t To get all DVDs type <list dvds>. \n"
        menu_list += "\t To get filtered rentals type <filter 'dvd name'>. \n"
        menu_list += "\t To add a new DVD type <adddvd 'dvd id' 'dvd name'>. \n"
        menu_list += "\t To add a new rental type <add 'dvd id' 'client name'>. \n"
        menu_list += "\t To return a rental type <ret 'dvd id'>. \n"
        
        menu_list += "\t To show the menu type <menu>.\n"
        menu_list += "\t To exit type <exit>.\n"
        print (menu_list)
        
    def print_list(self, myList):
        if len(myList) == 0:
            print("The list is empty!\n")
        else:
            for i in myList:
                print(i)
    
    def print_dvds_with_status(self):
        dvds = self.__ctrl.get_dvds_with_status()
        if len(dvds) == 0:
            print("No DVDs in the system!\n")
        else:
            print(f"{'ID':<6} {'Name':<25} {'Client':<15} {'Rented Date':<18} {'Return Date':<18} {'Status':<10}")
            print("-" * 95)
            for d in dvds:
                print(f"{d['id']:<6} {d['name']:<25} {d['client']:<15} {d['rented_date']:<18} {d['return_date']:<18} {d['status']:<10}")
    
    def print_rentals(self):
        rentals = self.__ctrl.list_rentals()
        if len(rentals) == 0:
            print("No active rentals!\n")
        else:
            print(f"{'ID':<6} {'DVD Name':<25} {'Client':<15} {'Rented Date':<18} {'Return Date':<18}")
            print("-" * 85)
            for r in rentals:
                print(f"{r.get_id():<6} {r.get_dvd_name():<25} {r.get_client_name():<15} {r.get_rented_date():<18} {r.get_return_date():<18}")
            
    def run(self):
        self.menu()
        while True:
            command = input("Please give me a command:")
            if command == "menu":
                self.menu()
            elif command == "list rentals":
                self.print_rentals()
            elif command == "list dvds":
                self.print_dvds_with_status()
            elif command == "exit":
                print("The program will exit...")
                return
            elif "filter" in command:
                info = command.split(" ", 1)
                if len(info) == 2:
                    self.print_list(self.__ctrl.filter_dvds_name(info[1]))
                else:
                    print("Please give me a valid command! \n")
            elif command.startswith("adddvd"):
                info = command.split(" ", 2)
                if len(info) == 3:
                    try:
                        self.__ctrl.add_new_dvd(int(info[1]), info[2])
                        print("Successfully added a new DVD. \n")
                    except DuplicateException as de:
                        print(de)
                    except ValueError:
                        print("DVD ID must be a number. \n")
                else:
                    print("Please give me a valid command! \n")
            elif command.startswith("add"):
                info = command.split(" ")
                if len(info) >= 3:
                    try:
                        rented_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                        return_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
                        self.__ctrl.add_new_borrow(info[2], info[1], rented_date, return_date)
                        print("Successfully rented a dvd. \n")
                    except DuplicateException as de:
                        print(de)  
                    except InexistingException as ie:
                        print (ie)  
                    except AlreadyBurrowed as ae:
                        print(ae)
                else:
                    print("Please give me a valid command! \n")
            elif "ret" in command:
                info = command.split(" ")
                try:
                    self.__ctrl.delete_borrow(int(info[1]))
                    print("Successfully returned a rented a dvd. \n")
                except InexistingException as ie:
                    print (ie)
            else:
                print("Please give me a valid command! \n") 
            
            
                        

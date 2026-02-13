from datetime import datetime


class Borrow():
    def __init__(self, id, idDvD, nameClient, rented_date=None, return_date=None):
        self.__id = id
        self.__idDvd = idDvD
        self.__nameClient = nameClient
        self.__rented_date = rented_date or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.__return_date = return_date or ""
    
    def get_id(self):
        return self.__id
    
    def get_id_dvd(self):    
        return self.__idDvd
    
    def get_name_client(self):
        return self.__nameClient
    
    def get_rented_date(self):
        return self.__rented_date
    
    def get_return_date(self):
        return self.__return_date
    
    def set_id(self, id): 
        self.__id = id
    
    def set_id_dvd(self, idDvd):
        self.__idDvd = idDvd
        
    def set_name_client(self, nameClient):
        self.__nameClient = nameClient
    
    def set_rented_date(self, rented_date):
        self.__rented_date = rented_date
    
    def set_return_date(self, return_date):
        self.__return_date = return_date
        
    def __str__(self): 
        return (str(self.__id) + " " + self.__nameClient + " " + str(self.__idDvd))

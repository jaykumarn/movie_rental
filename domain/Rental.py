class Rental():
   
    def __init__(self, idRental, dvd_name, client_name, rented_date="", return_date=""):
        self.__idRental = idRental
        self.dvd_name = dvd_name
        self.__client_name = client_name
        self.__rented_date = rented_date
        self.__return_date = return_date
        
    def get_id(self):
        return self.__idRental
    
    def get_dvd_name(self):
        return self.dvd_name
    
    def get_client_name(self):
        return self.__client_name
    
    def get_rented_date(self):
        return self.__rented_date
    
    def get_return_date(self):
        return self.__return_date
    
    def set_id(self, value): 
        self.__idRental = value
        
    def set_dvd_name(self, value):
        self.dvd_name = value
        
    def set_client_name(self, value): 
        self.__client_name = value
    
    def set_rented_date(self, value):
        self.__rented_date = value
    
    def set_return_date(self, value):
        self.__return_date = value
        
    def __str__(self):
        return (str(self.__idRental) + " " + str(self.dvd_name) + " " + str(self.__client_name))

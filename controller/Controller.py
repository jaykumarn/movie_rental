from domain.Borrow import Borrow
from domain.Rental import Rental 
from repository.BorrowRepository import BorrowRepository
from repository.DvdRepository import DvdRepository
from domain.Dvd import Dvd
from random import randint
from domain.Errors import DuplicateException, InexistingException, AlreadyBurrowed


class Controller():
    def __init__(self,borepo,dvdrepo):
        self.__borepo = borepo
        self.__dvdrepo = dvdrepo
        
    def list_rentals(self): 
        rentals = []
        
        for i in self.__borepo.get_all():
            dvd_idx = self.__dvdrepo.find(i.get_id_dvd())
            if dvd_idx != -1:
                dvd_name = self.__dvdrepo.get_all()[dvd_idx].get_name()
                r = Rental(i.get_id(), dvd_name, i.get_name_client(), 
                          i.get_rented_date(), i.get_return_date())
                rentals.append(r)

        rentals = sorted(rentals, key=lambda x: x.dvd_name)    
        return rentals
    
    def get_dvds_with_status(self):
        result = []
        borrowed_dvds = {}
        for b in self.__borepo.get_all():
            borrowed_dvds[b.get_id_dvd()] = b
        
        for dvd in self.__dvdrepo.get_all():
            dvd_id = dvd.get_id_dvd()
            if dvd_id in borrowed_dvds:
                borrow = borrowed_dvds[dvd_id]
                result.append({
                    'id': dvd_id,
                    'name': dvd.get_name(),
                    'client': borrow.get_name_client(),
                    'rented_date': borrow.get_rented_date(),
                    'return_date': borrow.get_return_date(),
                    'status': 'Rented'
                })
            else:
                result.append({
                    'id': dvd_id,
                    'name': dvd.get_name(),
                    'client': '',
                    'rented_date': '',
                    'return_date': '',
                    'status': 'Available'
                })
        return result 
    
    def filter_dvds_name(self, filterString):
        filteredList = []
        for dvd in self.__dvdrepo.get_all():
            if filterString.lower() in dvd.get_name().lower():
                filteredList.append(dvd)
        return filteredList
    
    def __get_all_borrow_ids(self):
        idsList = []
        for i in self.__borepo.get_all():
            idsList.append(i.get_id())
        return idsList
        
                   
    def add_new_borrow(self, name, dvd_id, rented_date=None, return_date=None):
        rand_ids = self.__get_all_borrow_ids()
        id = randint(0, max(len(rand_ids)*10, 100))
        while id in rand_ids:
            id = randint(0, max(len(rand_ids)*10, 100))
        if int(dvd_id) in self.__get_all_dvds_ids():
            if int(dvd_id) not in self.__get_all_dvds_ids_from_borrows():
                b = Borrow(int(id), int(dvd_id), name, rented_date, return_date)
                self.__borepo.add(b)
            else:
                raise AlreadyBurrowed()
        else:
            raise InexistingException()
        
    def delete_borrow(self, idBorrow):
        self.__borepo.remove(idBorrow)
        
    def __get_all_dvds_ids_from_borrows(self):
        dvdIds = []
        for b in self.__borepo.get_all():
            dvdIds.append(b.get_id_dvd())
        return dvdIds
        
              
    def __get_all_dvds_ids(self): 
        dvdIds = []
        for i in self.__dvdrepo.get_all():
            dvdIds.append(i.get_id_dvd())
        return dvdIds
    
    def add_new_dvd(self, dvd_id, name):
        dvd = Dvd(int(dvd_id), name)
        self.__dvdrepo.add(dvd)
    
    def get_all_dvds(self):
        return self.__dvdrepo.get_all()
        
        
    
    
        
    
"""      
def test():
    BorrowRepo = BorrowRepository()
    newBor = Borrow(5,7,"ajska")
    BorrowRepo.add(newBor)
    newBor = Borrow(1,2,"asdfas")
    BorrowRepo.add(newBor)
    newBor = Borrow(2,1,"hurrdurr")
    BorrowRepo.add(newBor)
    
    DvdRepo = DvdRepository()
    newDvd = Dvd(2,"hkasf")
    DvdRepo.add(newDvd)
    newDvd = Dvd(1,"hkdss")
    DvdRepo.add(newDvd)
    newDvd = Dvd(7,"hk98098080")
    DvdRepo.add(newDvd)
    
    ctrl = Controller(BorrowRepo,DvdRepo) 
    
    for r in ctrl.show_all_rentals():
        print (r)
        
        
test()
"""    
    
    
    
       
     
            
            
            
            
        
        
            
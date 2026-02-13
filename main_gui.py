from repository.BorrowRepository import BorrowRepository
from repository.DvdRepository import DvdRepository
from controller.Controller import Controller
from ui.GraphicalUI import MovieRentalGUI


def main():
    borrow_repo = BorrowRepository("borrow.txt")
    dvd_repo = DvdRepository("dvd.txt")
    
    controller = Controller(borrow_repo, dvd_repo)
    gui = MovieRentalGUI(controller)
    gui.run()


if __name__ == "__main__":
    main()

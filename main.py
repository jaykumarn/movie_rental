from repository.BorrowRepository import BorrowRepository
from repository.DvdRepository import DvdRepository
from controller.Controller import Controller
from ui.UI import UI


def main():
    borrow_repo = BorrowRepository("borrow.txt")
    dvd_repo = DvdRepository("dvd.txt")
    
    ctrl = Controller(borrow_repo, dvd_repo)
    
    print("\nSelect interface:")
    print("1. Command Line Interface")
    print("2. Graphical User Interface")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        from ui.GraphicalUI import MovieRentalGUI
        gui = MovieRentalGUI(ctrl)
        gui.run()
    else:
        ui = UI(ctrl)
        ui.run()


if __name__ == "__main__":
    main()
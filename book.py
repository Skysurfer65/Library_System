import datetime
from dateutil.relativedelta import relativedelta

class Book():
    '''
    A Class to create books and book representation
    '''
    categories = {'Literature','Science','Entertainment'}
    def __init__(self,title,Auther_name,ISBN,status_week,category) -> None:
        self.title = title
        self.auther_name = Auther_name
        self.isbn = ISBN
        # *** Changed to isocalender object to fix bugg around new year ***
        self.status_week = datetime.date.today().isocalendar() 
        # Check category
        if category in self.categories:
            self.category = category
        else:
            raise ValueError("Bad input Book Category")
        self.borrowed = False # Added for simplicity
    @classmethod
    def literature_book(cls,title,Auther_name,ISBN,status_week):
        return cls(title,Auther_name,ISBN,\
                   datetime.date.today().isocalendar(),'Literature')
    @classmethod
    def Science_book(cls,title,Auther_name,ISBN,status_week):
        return cls(title,Auther_name,ISBN,\
                   datetime.date.today().isocalendar(),'Science')
    @classmethod
    def Entertainment_book(cls,title,Auther_name,ISBN,status_week):
        return cls(title,Auther_name,ISBN,\
                   datetime.date.today().isocalendar(),'Entertainment')
    def __repr__(self) -> str:
        out_put = f"Book Title = {self.title}\n"+\
                  f"Book Auther name = {self.auther_name}\n"+\
                  f"Book ISBN = {self.isbn}\n"+\
                  f"Book Category = {self.category}\n"
        current_week = datetime.date.today().isocalendar()
        if self.status_week > current_week : # Bugg fixed
            out_put += f"Book is borrowed till week# {self.status_week[1]}"
        else:
            out_put += f"Book is available fr.o.m week# {self.status_week[1]}"    
        return out_put
    def is_available(self):
        current_week = datetime.date.today().isocalendar()
        if self.status_week > current_week :# Bugg fixed
            return False
        else:
            return True
    def borrow_book(self,weeks):
        if self.is_available() and weeks >0 :
            self.status_week = (datetime.date.today() + relativedelta(weeks=weeks)).isocalendar() # Bugg fixed
            return True
        else:
            raise Exception("Bad value weeks")

    def return_book(self):
        current_week = datetime.date.today().isocalendar() # Bugg fix
        self.status_week = current_week




from book import Book
from borrower import Borrower
import re
import json

class MyLibraryApp():
    '''
    This is the Class that creates a library app and interacts with Book and Borrower Class
    '''
    #class variables
    id_counter = 0   
    menu_text = '''
    ******** Library Menu *******\n
    Register a new borrower choose "B"
    Add a new book to our library choose "A"
    Lend out or rent out a book choose "L"
    Return a book choose "R"
    Print out all library books "P"
    Print out library status "S"
    To quit write "Q"\n
    '''
    def __init__(self) -> None:
        self.books_DB = dict()
        self.borrower_DB = dict()
        self.id_counter = 0
        self.receivables = 0
        self.cash = 0

    def set_up_DB(self):
        # load JSON books file or create if not avail
        try:
             with open('books_DB.json', 'r') as f:
                books_json = f.read()
                nested_books = json.loads(books_json)
                # This will reset status_week and borrowed bool according to Book constructor
                # TODO rewrite program to show correct status
                for book in nested_books:
                    self.books_DB[book] = Book(nested_books[book]['title'],nested_books[book]['auther_name'],
                    nested_books[book]['isbn'],nested_books[book]['status_week'],nested_books[book]['category'])
        except FileNotFoundError:
            # Create new JSON
            with open('books_DB.json', 'w') as f:
                f.write(json.dumps({}))       
               
    def menu_input(self):
        while True:
            print(self.menu_text)    
            user_input = input("What is your choice: ")
            checked_input = re.match('\Ab|a|l|r|p|s|q', user_input, flags=re.IGNORECASE)
            if checked_input is None:
                print('\nSomething went wrong, you can only choose letters from the menu!!! try again.....')
            else:
                break
        return user_input.upper() 

    def menu_choices(self):      
        while True:
            user_input = self.menu_input()
            if user_input == 'B':
                self.new_borrower()
            elif user_input == 'A':
                self.add_book()
            elif user_input == 'L':
                self.lend_out_book()
            elif user_input == 'R':
                self.return_book()
            elif user_input == 'P':
                self.print_all_books()
            elif user_input == 'S':
                self.library_status()
            elif user_input == 'Q':
                break
        self.exit_library()    
                      
    def validated_input(self, check_regex, text):
        while True:
            user_input = input(text)
            checked_input = re.match(check_regex, user_input, flags=re.IGNORECASE)
            if checked_input is None:
                print('\nSomething went wrong, make a valid input, try again.....')
            else:
                break    
        return user_input.lower()

    def new_borrower(self):
        name = input('Enter borrowers name: ')
        # validation via validated_input
        text = 'Is borrower a student, "y" or "n": '
        student = self.validated_input('\Ay|n', text)
        text = 'Is borrower a teacher, "y" or "n": '
        teacher = self.validated_input('\Ay|n', text)
        # Set bools
        if student == 'y': student = True
        else: student = False
        if teacher == 'y': teacher = True
        else: teacher = False
        self.id_counter += 1
        #Create borrower try with @classmethods
        if student and not teacher:
            borrower = Borrower.borrower_student(name, self.id_counter)
        elif teacher and not student:
            borrower = Borrower.borrower_teacher(name, self.id_counter)
        else:
            borrower = Borrower(name, self.id_counter, student, teacher)
 
        # Add borrower to dictionary
        self.borrower_DB[self.id_counter] = borrower   
        print(f"Your ID for lending books is {self.id_counter}")
        
    def add_book(self):
        title = input("What is the book title: ")
        author_name = input("What is the author name: ")
        isbn = input("What is the ISBN number: ")
        category = input("what is the category of the book, you can choose from 'Literature','Science','Entertainment': ").capitalize()
        try:
            new_book = Book(title, author_name, isbn, None, category)
        except ValueError as e:
            print(e)
        else:
            self.books_DB[isbn] = new_book

    def lend_out_book(self):
        weeks, charges = 0, 0
        text = "What is your borrower ID: "
        # Max number of borrower_id is 9
        borrower_id = self.validated_input('[1-9]', text)
        if int(borrower_id) in self.borrower_DB:          
            print(self.borrower_DB[int(borrower_id)])
            print("Which book are you interested in, choose ISBN from our list:\n"+"*"*60)
        else: 
            print("**** Sorry, can't find your ID  ****")
            self.menu_choices()

        self.print_all_books()
        borrower_choice = input("\nChoose book by ISBN number: ")
        if borrower_choice not in self.books_DB:
            print("**** Sorry, can't find the ISBN item, check inventory ****")
            self.menu_choices()
        # New instance of Book 
        # TODO find better way for polymorphism issues, this works but doesn't look good
        book = self.books_DB[borrower_choice]
        # Check if book available
        if book.borrowed:
            print("Book is out, check inventory when available")
            self.menu_choices()
        book = Book(book.title, book.auther_name, book.isbn, None, book.category)
        # New instance of borrower
        borrower = self.borrower_DB[int(borrower_id)]
        borrower = Borrower(borrower.b_name, borrower.b_id, borrower.is_student, borrower.is_teacher)
        # Weeks and charges
        # If borrower is both student and teacher, student charges applies
        if borrower.is_student or borrower.is_teacher:      
            if book.category == "Literature":
                if borrower.is_student:
                    weeks = 4
                    charges = 0
                elif borrower.is_teacher:
                    weeks = 4
                    charges = 10
            elif book.category == "Science":
                if borrower.is_student:
                    weeks = 4
                    charges = 5
                elif borrower.is_teacher:
                    weeks = 2
                    charges = 15
            elif book.category == "Entertainment":
                weeks = 3
                charges = 0
            try:
                book.borrow_book(weeks)
            except Exception as e:
                print(e)
                self.menu_choices()
            borrower.charges += charges
            book.borrowed = True
            self.books_DB[borrower_choice] = book
            self.borrower_DB[int(borrower_id)] = borrower
            self.receivables += charges               
        else: print("Borrower has to be student and/or teacher to borrow a book")             

    def return_book(self):
        isbn = input("Enter the ISBN number for the book to be returned: ")
        if isbn not in self.books_DB:
            print("**** Sorry, can't find ISBN item, check inventory ****")
            self.menu_choices()
        book = self.books_DB[isbn]

        text = "What is your borrower ID: "
        borrower_id = self.validated_input('[1-9]', text)
        if int(borrower_id) not in self.borrower_DB:
            print("**** Sorry, your ID is not valid ****")
            self.menu_choices() 
        borrower = self.borrower_DB[int(borrower_id)]

        print(f"You owe us {borrower.charges} SEK")
        self.cash += borrower.charges
        self.receivables -= borrower.charges
        # Clean up
        borrower.charges = 0
        book.borrowed = False
        book.return_book()

    def print_all_books(self):
        for book in self.books_DB:
            print(self.books_DB[book])
            print()     

    def library_status(self):
        # How many books are out
        num_of_books_out = 0
        for book in self.books_DB:
            if self.books_DB[book].borrowed:
                num_of_books_out += 1
        print(f"Our library has {self.cash} SEK in funds and {self.receivables} SEK in recievables.\n"+\
            f"We have a total of {len(self.books_DB)} books and {num_of_books_out} are lended out")

    def exit_library(self):
        # Save books dictionary to repository file 
        json_books = json.dumps(self.books_DB, default=lambda o: o.__dict__)
        with open('books_DB.json', 'w') as f:
            f.write(json_books)
        print("Bye bye, see you next time :-)")
       
####### To be run #######
if __name__=='__main__':   
    school_library = MyLibraryApp()
    school_library.set_up_DB()
    school_library.menu_choices()
    
    

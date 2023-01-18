from new_library_app import MyLibraryApp
from book import Book
from borrower import Borrower
import datetime
from dateutil.relativedelta import relativedelta
from unittest import TestCase
from unittest.mock import patch

class MyLibraryAppTest(TestCase):

    def test_constructor_my_library_app(self):
        # Test variable
        library_instance = MyLibraryApp()
        num_of_attr = len(library_instance.__dict__)
        # Tests
        self.assertIsInstance(library_instance.books_DB, dict)
        self.assertEqual(0, len(library_instance.books_DB))
        self.assertIsInstance(library_instance.borrower_DB, dict)
        self.assertEqual(0, len(library_instance.borrower_DB))
        self.assertEqual(0, library_instance.id_counter)
        self.assertEqual(0, library_instance.receivables)
        self.assertEqual(0, library_instance.cash)
        self.assertEqual(5, num_of_attr)
        
    def test_menu_input(self):
        # Test variable
        library_instance = MyLibraryApp()
        expected = '\n    ******** Library Menu *******\n\n    Register a new borrower choose "B"\n'+\
            '    Add a new book to our library choose "A"\n    Lend out or rent out a book choose "L"\n'+\
                '    Return a book choose "R"\n    Print out all library books "P"\n    Print out library status "S"\n'+\
                    '    To quit write "Q"\n\n    '
    
        # Patch input and assert
        with patch('builtins.input', return_value = 'b'):
            result = library_instance.menu_input()
            self.assertEqual('B', result)
        
        with patch('builtins.input', return_value = 'A'):
            with patch ('builtins.print') as mocked_print:
                library_instance.menu_input()
                mocked_print.assert_called_with(expected)
                      
    def test_menu_choices(self):
        # Test variables
        library_instance = MyLibraryApp()
        expected = '\n    ******** Library Menu *******\n\n    Register a new borrower choose "B"\n'+\
            '    Add a new book to our library choose "A"\n    Lend out or rent out a book choose "L"\n'+\
                '    Return a book choose "R"\n    Print out all library books "P"\n    Print out library status "S"\n    To quit write "Q"\n\n    '
        # Patch exit_library to not overwright JSON
        with patch('new_library_app.MyLibraryApp.exit_library') as mocked_exit:
            # Patch print and keyboard
            with patch('builtins.print') as mocked_print:
                with patch('builtins.input') as mocked_input:
                    mocked_input.side_effect = ('P', 'Q')
                    library_instance.menu_choices()
                    mocked_print.assert_called()
                    mocked_exit.assert_called_once()
            # Patch choice 'B' and go through all inputs then quit
            with patch('builtins.print') as mocked_print:
                with patch('builtins.input') as mocked_input:
                    mocked_input.side_effect = ('B','Bax','y','n', 'Q')
                    library_instance.menu_choices()
                    mocked_print.assert_called_with(expected)
                    mocked_exit.assert_called()
                    self.assertEqual('Bax', library_instance.borrower_DB[1].b_name)
                
    def test_validated_input(self):
        # Test variable
        library_instance = MyLibraryApp()
        test_regex = '\Ay|n'
        with patch('builtins.input',return_value = 'Y') as mocked_input:
            result = library_instance.validated_input(test_regex, 'something')
            mocked_input.assert_called()          
            self.assertEqual('y', result)

    def test_new_borrower(self):
        # Test variables
        library_instance = MyLibraryApp()
        expected_1 = {'b_name': 'Bax', 'b_id': 1, 'is_student': True, 'is_teacher': False, 'charges': 0}
        expected_2 = {'b_name': 'Sture', 'b_id': 2, 'is_student': False, 'is_teacher': True, 'charges': 0}
        # Setup and assertion
        with patch('builtins.input') as mocked_input: 
            mocked_input.side_effect = ('Bax','y','n')
            library_instance.new_borrower()
        self.assertEqual(1, len(library_instance.borrower_DB))
        self.assertEqual(expected_1, library_instance.borrower_DB[1].__dict__)        
        with patch('builtins.input') as mocked_input: 
            mocked_input.side_effect = ('Sture','n','y')
            library_instance.new_borrower()
        self.assertEqual(2, len(library_instance.borrower_DB))
        self.assertEqual(expected_2, library_instance.borrower_DB[2].__dict__) 

    def test_add_book(self):
        # Test variables
        library_instance = MyLibraryApp()
        isbn = '111111111'
        current_week = datetime.date.today().isocalendar()
        expected_1 = {'title': 'Flying', 'auther_name': 'Anders Andersson', 'isbn': '111111111',
                 'status_week': current_week, 'category': 'Science', 'borrowed': False}
        expected_2 = 'Bad input Book Category'
        # Setup and assertion
        with patch('builtins.input') as mocked_input: 
            mocked_input.side_effect = ('Flying','Anders Andersson',isbn, 'science')
            library_instance.add_book()
        self.assertEqual(1, len(library_instance.books_DB))
        self.assertEqual(expected_1, library_instance.books_DB[isbn].__dict__)
        with patch('builtins.input') as mocked_input: 
            with patch ('builtins.print') as mocked_print:
                mocked_input.side_effect = ('Flying','Anders Andersson',isbn, 'Agriculture')
                library_instance.add_book()
                self.assertRaises(ValueError)
                mocked_print.assert_called()
                
        #mocked_print.assert_called_with(expected_2)
        self.assertEqual(1, len(library_instance.books_DB))     
    
    def test_lend_out_book(self):
        # Test variables
        library_instance = MyLibraryApp()
        library_instance.books_DB['111111111'] = Book('Flying','Anders Andersson','111111111',None,'Science')
        library_instance.borrower_DB[1] = Borrower('Bax',1,True,False)  
        # Datetime 4 weeks ahead
        four_weeks_ahead = (datetime.date.today() + relativedelta(weeks=4)).isocalendar()  

        # Setup and assertion
        self.assertEqual(1, len(library_instance.borrower_DB))
        self.assertEqual(1, len(library_instance.books_DB))
        
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('1','111111111')       
            library_instance.lend_out_book()
            mocked_input.assert_called_with('\nChoose book by ISBN number: ')

        self.assertEqual(5, library_instance.borrower_DB[1].charges)
        self.assertEqual(four_weeks_ahead, library_instance.books_DB['111111111'].status_week)
        self.assertTrue(library_instance.books_DB['111111111'].borrowed)
           
    def test_return_book(self):
        # Test variables
        library_instance = MyLibraryApp()
        borrower = Borrower('Bax',1,True,False)
        book = Book('Flying','Anders Andersson','111111111',None,'Science')
        book.borrowed = True
        borrower.charges = 5
        library_instance.borrower_DB[1] = borrower
        library_instance.books_DB['111111111'] = book
    
        # Setup and assertion
        with patch('builtins.input') as mocked_input: 
            mocked_input.side_effect = ('111111111','1')
            library_instance.return_book()
        self.assertEqual(5, library_instance.cash)
        self.assertEqual(0, borrower.charges)
        self.assertFalse(book.borrowed)
          
    def test_print_all_books(self):
        # Test variables
        library_instance = MyLibraryApp()
        library_instance.books_DB = {'111111111': {'title': 'Flying', 'auther_name': 'Anders Andersson', 'isbn': '111111111',
                            'status_week': '52', 'category': 'Science', 'borrowed': False}}
        # Patch the output
        with patch('builtins.print') as mocked_print:
            library_instance.print_all_books()
            mocked_print.assert_called()
            mocked_print.assert_called_with() # Last call is empty print() for estetics
        
    def test_library_status(self):
        # Test variables
        library_instance = MyLibraryApp()
        #library_instance.borrower_DB = { 1: {'b_name': 'Bax', 'b_id': 1, 'is_student': True, 'is_teacher': False}}
        book = Book('Flying', 'Bax Fling', '111111111', None, 'Science')
        library_instance.books_DB['111111111'] = book
        # Patch the printouts
        with patch('builtins.print') as mocked_print:
            library_instance.library_status()
            mocked_print.assert_called()
            mocked_print.assert_called_with("Our library has 0 SEK in funds and 0 SEK in recievables.\n"+\
                "We have a total of 1 books and 0 are lended out")
            
        

    def test_exit_library(self):
        # Test variables
        library_instance = MyLibraryApp()
        # Patch exit_library to not overwright JSON
        with patch('new_library_app.MyLibraryApp.exit_library') as mocked_exit:
            library_instance.exit_library()
            mocked_exit.assert_called_once()
               
            
   

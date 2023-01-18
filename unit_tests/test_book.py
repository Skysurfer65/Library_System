from unittest import TestCase
from book import Book
import datetime
from dateutil.relativedelta import relativedelta

class BookTest(TestCase):
    # Test constructor of Book class
    def test_constructor_book(self):
        # Test variables
        book_instance = Book('Flying', 'Richard Fehling', '123456789', None, 'Science')
        num_of_attr = len(book_instance.__dict__)
        # Create instance of now via datetime
        instance_of_now = datetime.date.today().isocalendar()

        # Run tests
        self.assertEqual(6, num_of_attr)
        self.assertEqual('Flying', book_instance.title)
        self.assertEqual('Richard Fehling', book_instance.auther_name)
        self.assertEqual('123456789', book_instance.isbn)
        self.assertEqual(instance_of_now, book_instance.status_week)
        self.assertEqual('Science', book_instance.category)
        # Test of constructor if - statement
        with self.assertRaises(ValueError) as msg:
            Book('Flying', 'Richard Fehling', '123456789', None, 'Gastronomic')
        the_exception = str(msg.exception)
        self.assertEqual(the_exception, 'Bad input Book Category')
        self.assertFalse(book_instance.borrowed)    

    # Test @classmethods
    def test_literature_book(self):
        # Test variables
        book_inst_literature = Book.literature_book('Thrills of Python', 'John Doe', '987654321', None)
        instance_of_now = datetime.date.today().isocalendar()

        # Run tests
        self.assertEqual('Thrills of Python', book_inst_literature.title)
        self.assertEqual('John Doe', book_inst_literature.auther_name)
        self.assertEqual('987654321', book_inst_literature.isbn)
        self.assertEqual(instance_of_now, book_inst_literature.status_week)
        self.assertEqual('Literature', book_inst_literature.category)

    def test_Science_book(self):
        # Test variables
        book_inst_science = Book.Science_book('Why Python?', 'John Doe', '000000000', None)
        instance_of_now = datetime.date.today().isocalendar()

        # Run tests
        self.assertEqual('Why Python?', book_inst_science.title)
        self.assertEqual('John Doe', book_inst_science.auther_name)
        self.assertEqual('000000000', book_inst_science.isbn)
        self.assertEqual(instance_of_now, book_inst_science.status_week)
        self.assertEqual('Science', book_inst_science.category)

    def test_Entertainment_book(self):
        # Test variables
        book_inst_entertainment = Book.Entertainment_book('Python is fun', 'John Doe', '111111111', None)
        instance_of_now = datetime.date.today().isocalendar()

        # Run tests
        self.assertEqual('Python is fun', book_inst_entertainment.title)
        self.assertEqual('John Doe', book_inst_entertainment.auther_name)
        self.assertEqual('111111111', book_inst_entertainment.isbn)
        self.assertEqual(instance_of_now, book_inst_entertainment.status_week)
        self.assertEqual('Entertainment', book_inst_entertainment.category)
    

    # Test string representation of Book class objects
    def test_repr(self):
        # Test variables
        book_instance = Book('Flying', 'Richard Fehling', '123456789', None, 'Science')
        # Create instance of now via datetime
        instance_of_now = datetime.date.today().isocalendar()
        # Create instance of one week ahead
        one_week_ahead = (datetime.date.today() + relativedelta(weeks=1)).isocalendar()

        # Expected outputs
        book_avail = "Book Title = Flying\nBook Auther name = Richard Fehling\nBook ISBN = 123456789\n"+\
            f"Book Category = Science\nBook is available fr.o.m week# {instance_of_now[1]}"

        book_not_avail = "Book Title = Flying\nBook Auther name = Richard Fehling\nBook ISBN = 123456789\n"+\
            f"Book Category = Science\nBook is borrowed till week# {one_week_ahead[1]}"

        # Run tests with book available
        self.assertEqual(book_avail, book_instance.__repr__())

        # Run test with status_week + 1 from now 
        book_instance.status_week = one_week_ahead
        self.assertEqual(book_not_avail,book_instance.__repr__())
        

    # Test is_available function
    def test_is_available(self):
        # Test variables
        book_instance = Book('Flying', 'Richard Fehling', '123456789', None, 'Science')
        one_week_ahead = (datetime.date.today() + relativedelta(weeks=1)).isocalendar()
        
        # Run test with book available
        self.assertTrue(book_instance.is_available())

        # Run test with status_week + 1 from now 
        book_instance.status_week = one_week_ahead
        self.assertFalse(book_instance.is_available())




    # Test borrow_book function
    def test_borrow_book(self):
        # Test variables
        book_instance = Book('Flying', 'Richard Fehling', '123456789', None, 'Science')
        two_weeks = 2
        two_weeks_ahead = (datetime.date.today() + relativedelta(weeks=2)).isocalendar()
        three_weeks = 3
        three_weeks_ahead = (datetime.date.today() + relativedelta(weeks=3)).isocalendar()
        four_weeks = 4
        four_weeks_ahead = (datetime.date.today() + relativedelta(weeks=4)).isocalendar()

        # Run tests for different borrowing time
        book_instance.borrow_book(two_weeks)
        self.assertEqual(two_weeks_ahead, book_instance.status_week)
        # Reset status_week
        book_instance.status_week = datetime.date.today().isocalendar()
        self.assertTrue(book_instance.borrow_book(three_weeks))
        self.assertEqual(three_weeks_ahead, book_instance.status_week)
        # Reset status_week
        book_instance.status_week = datetime.date.today().isocalendar()
        self.assertTrue(book_instance.borrow_book(four_weeks))
        self.assertEqual(four_weeks_ahead, book_instance.status_week)
        
        # Run test of first if-statement 
        with self.assertRaises(Exception) as msg:
            book_instance.borrow_book(-1)
        the_exception = str(msg.exception)
        self.assertEqual(the_exception, "Bad value weeks") 
        
    # Test return_book function
    def test_return_book(self):
        # Test variables
        book_instance = Book('Flying', 'Richard Fehling', '123456789', None, 'Science')
        instance_of_now = datetime.date.today().isocalendar()
        three_weeks_ahead = (datetime.date.today() + relativedelta(weeks=3)).isocalendar()
        # Setup
        book_instance.status_week = three_weeks_ahead
        book_instance.return_book()

        # Run test
        self.assertEqual(instance_of_now, book_instance.status_week)

    # Test class Set variable
    def test_class_variable(self):
        self.assertSetEqual({'Literature','Science','Entertainment'}, Book.categories)



        
        

        
        

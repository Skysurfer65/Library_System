from new_library_app import MyLibraryApp
from book import Book
from borrower import Borrower
from unittest import TestCase
from unittest.mock import patch
import json

class MyLibrarySystemTest(TestCase):
    
    def test_school_library(self):
        # Make instance of MyLibraryApp
        test_library = MyLibraryApp()

        # Load or write JSON
        test_library.set_up_DB()
        books_in_repo = len(test_library.books_DB)

        # Add book and borrower to library, keyboard sequence 
        add_book = ('A','Building Machines','Frida Fridolfsson',
        'xxxxxxxxx','Science','B','Richard Fehling','y','n','Q')

        #with patch('builtins.print') as mocked_keyboard:
        with patch('builtins.input') as mocked_keyboard:
            mocked_keyboard.side_effect = (add_book)
            test_library.menu_choices()
               
        # Assert and evaluate
        # Borrower has been added
        self.assertEqual(1, len(test_library.borrower_DB))
        expected = Borrower('Richard Fehling',1,True,False)
        self.assertDictEqual(expected.__dict__,test_library.borrower_DB[1].__dict__)

        # Book has been added
        with open('books_DB.json', 'r') as f:
            books_json = f.read()
            nested_books = json.loads(books_json)

        books_in_updated_repo = books_in_repo + 1
        self.assertEqual(books_in_updated_repo, len(nested_books))

        # Clean up
        del nested_books['xxxxxxxxx']
        books = dict()
        for book in nested_books:
            books[book] = Book(nested_books[book]['title'],nested_books[book]['auther_name'],
            nested_books[book]['isbn'],nested_books[book]['status_week'],nested_books[book]['category'])
        json_books = json.dumps(books, default=lambda o: o.__dict__)
        with open('books_DB.json', 'w') as f:
            f.write(json_books)
        




        
            
   

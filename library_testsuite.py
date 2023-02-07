from unittest import TestSuite, TextTestRunner
from unit_tests.test_book import BookTest
from unit_tests.test_borrower import BorrowerTest
from integration_tests.test_new_library_app import MyLibraryAppTest
from system_tests.test_new_library_system import MyLibrarySystemTest  

def suite():
    # Add specific test suites, "runner.run(suite())"
    # works by playbutton in VSC. CLI will run all tests
    suite = TestSuite()
    suite.addTest(BookTest('test_constructor_book'))
    suite.addTest(BorrowerTest('test_constructor_borrower'))
    suite.addTest(MyLibraryAppTest('test_constructor_my_library_app'))
    suite.addTest(MyLibrarySystemTest('test_school_library'))
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run()
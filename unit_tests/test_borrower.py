from unittest import TestCase
from borrower import Borrower

class BorrowerTest(TestCase):
    # Test constructor of Borrower class
    def test_constructor_borrower(self):
        # Test Variables
        student = Borrower('Richard Fehling', 1, is_student=True, is_teacher=False)
        teacher = Borrower('Bax Fling', 2, is_student=False, is_teacher=True)
        num_of_attr = len(student.__dict__)
        # Run tests
        self.assertEqual(5, num_of_attr)

        self.assertEqual('Richard Fehling', student.b_name)
        self.assertEqual(1 , student.b_id)
        self.assertTrue(student.is_student)
        self.assertFalse(student.is_teacher)

        self.assertEqual('Bax Fling', teacher.b_name)
        self.assertEqual(2 , teacher.b_id)
        self.assertTrue(teacher.is_teacher)
        self.assertFalse(teacher.is_student)

   
    def test_classmethod_student(self):
        # Test variables
        student = Borrower.borrower_student('Richard Fehling', 1)
        # Run tests
        self.assertEqual('Richard Fehling', student.b_name)
        self.assertEqual(1 , student.b_id)
        self.assertTrue(student.is_student)
        self.assertFalse(student.is_teacher)

    def test_classmethod_teacher(self):
        # Test variables
        teacher = Borrower.borrower_teacher('Bax Fling', 2)
        # Run tests
        self.assertEqual('Bax Fling', teacher.b_name)
        self.assertEqual(2 , teacher.b_id)
        self.assertTrue(teacher.is_teacher)
        self.assertFalse(teacher.is_student)

    def test_repr(self):
        # Test variables
        student = Borrower('Richard Fehling', 1, is_student=True, is_teacher=False)
        teacher = Borrower.borrower_teacher('Bax Fling', 2)
        # Expected output
        student_info = "Borrower Name: Richard Fehling\n"\
                       "Borrower ID: 1\n"\
                       "Borrower is Student"
        teacher_info = "Borrower Name: Bax Fling\n"\
                       "Borrower ID: 2\n"\
                       "Borrower is Teacher"
        # Run tests
        self.assertEqual(student_info, student.__repr__())
        self.assertEqual(teacher_info, teacher.__repr__())




from django.test import TestCase

class MyTest(TestCase):

    @classmethod
    def SetUpTest(cls):
        print("SetUpTest - Run test")

    def test_false_is_true(self):
        print('Method test_false_is_true - Run test')
        self.assertFalse(False)

    def test_one_plus_one_equals_two(self):
        print("Method test_one_plus_one_equals_two - run test")
        self.assertTrue(1 + 1, 2)


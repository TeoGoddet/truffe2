from django.test import TestCase

# Create your tests here.
class TruffeNoLoginTest(TestCase):
    
    def test_basic(self):
        self.assertTrue(True, "No view")

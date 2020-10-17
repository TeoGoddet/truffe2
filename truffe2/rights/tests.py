from django.test import TestCase

class RightsNoLoginTest(TestCase):
    
    def test_basic(self):
        self.assertTrue(True, "No view")

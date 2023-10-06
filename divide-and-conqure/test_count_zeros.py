from unittest import TestCase
from count_zeros import MyApp

class Test_Count_Zeros(TestCase):
   def test_count_zeros(self):
      myapp = MyApp()
      self.assertEqual(myapp.count_zeros([1,1,1,1,0,0]),2) 
      self.assertEqual(myapp.count_zeros([1,0,0,0,0]),4)
      self.assertEqual(myapp.count_zeros([0,0,0]),3)
      self.assertEqual(myapp.count_zeros([1,1,1,1]),0)
      self.assertEqual(myapp.count_zeros([1,1,1,1,1,1,1,1,1,1,1]),0)
      self.assertEqual(myapp.count_zeros([1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0]),9)
      
   def test_negative_test_case(self):
      myapp = MyApp()
      self.assertNotEqual(myapp.count_zeros([1,1,0,1,0,0]),3)
      self.assertNotEqual(myapp.count_zeros([1,1,0,1,0,0,1]),3)
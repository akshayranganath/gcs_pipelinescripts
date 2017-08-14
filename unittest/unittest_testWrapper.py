# -*- coding: utf-8 -*-
#!/usr/env python


import sys
import unittest

sys.path.append('functionaltests'); sys.path.append('../functionaltests')
from testWrapper import TestWrapper

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.wrapper = TestWrapper()

    def test_return_valid_ip(self):
        self.assertIsNotNone(self.wrapper.getIPAddress('www.akamai.com'),msg="Network error. Unable to resolve www.akamai.com")

    def test_return_no_ip(self):
        self.assertIsNone(self.wrapper.getIPAddress('a'),msg="Unknown error. 'a' has been resolved as a valid domain name")

    def test_is_site_accessible(self):
        response = self.wrapper.hostExists('www.akamai.com')
        #self.assertListEqual([200,301,302,404],msg="Failed to connect to website")
        self.assertTrue(response==True,msg="Failed to connect to website")

    def test_is_site_inaccessible(self):
        response = self.wrapper.hostExists('a')
        #self.assertListEqual([200,301,302,404],msg="Failed to connect to website")
        self.assertTrue(response==False,msg="Failed to connect to website")

if __name__=="__main__":
    unittest.main()
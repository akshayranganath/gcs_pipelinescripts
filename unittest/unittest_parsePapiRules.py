# -*- coding: utf-8 -*-
#!/usr/env python

'''
This is a function to test run some basic tests on a configuration file
'''

import unittest
import os
import sys

sys.path.append('functionaltests'); sys.path.append('../functionaltests')
from  parsePapiRules import FunctionalTests


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        #first create an instance of the functional test
        self.ft = FunctionalTests('rules.json','hostinfo.json')


    # Test 1: check if the rules file even exists
    def test_if_rules_file_exists(self):
        self.assertTrue(os.path.isfile(self.ft.filename))

    # Test 2: check if at least one host name is present
    def test_if_one_host_present(self):
        self.assertGreater(len(self.ft.getHostNames() ), 0 )

    # Test 3: check if at least one edge host name is present
    def test_if_one_edgehostname_present(self):
        self.assertGreater(len(self.ft.getEdgeHostNames() ) , 0)

    # Test 4: check if SR object defined
    def test_if_sr_object_defined(self):
        self.assertIsNotNone(self.ft.getSrObject())

    # Test 5: check if hosts file exists
    def test_if_host_file_exists(self):
        self.assertTrue(os.path.isfile(self.ft.hostsfile))

    # Test 6: find origin names
    def test_if_origins_defined(self):
        self.assertGreater( len(self.ft.getOriginDetals() ), 0)

    def tearDown(self):
        ft = None


if __name__=="__main__":
    unittest.main()
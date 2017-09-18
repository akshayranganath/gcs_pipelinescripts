# -*- coding: utf-8 -*-
#!/usr/env python

import unittest
from nose.tools import assert_equal
from parameterized import parameterized
import requests
import os


class TestBasicFunctionality(unittest.TestCase):

    def setUp(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip/deflate",
            "Connection": "keep-alive",
            "Accept-Language":"en-use",
            "Pragma": "akamai-x-get-cache-key"
        }

    def test_check_if_base_domain_defined(self):
        self.assertIn('DOMAIN',os.environ)

    @parameterized.expand([
        ("/", 200, None, "Home page - Response code failed"),
        ("/desktops", 200, None, "Category page - Response code failed"),
        ("/desktops/mac", 200, None, "Sub-cat page - Response code failed"),
        ("/desktops/mac/imac", 200, None, "PDP - Response code failed"),
        ("/",None,"000","Home page - cache test failed"),
        ("/desktops", None, "000", "Category page - cache test failed"),
        ("/desktops/mac", None, "000", "Sub-cat page - cache test failed"),
        ("/desktops/mac/imac", None, "000", "PDP - cache test failed")
    ])
    def test_request_status_code(self,url, expected_status_code, expected_ttl, error_message):
        if 'DOMAIN' in os.environ:
            self.headers['Host'] = os.environ['DOMAIN']
            response = requests.get('http://a1.b.akamai-staging.net'+ url, headers=self.headers)
            if expected_status_code != None:
                assert_equal(response.status_code, expected_status_code, msg=error_message)
            else:
                ttl = response.headers['X-Cache-Key'].split('/')[4]
                assert_equal(expected_ttl, ttl, msg=error_message)


if __name__ == "__main__":
    unittest.main()
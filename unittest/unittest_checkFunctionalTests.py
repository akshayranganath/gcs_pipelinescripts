# -*- coding: utf-8 -*-
#!/usr/env python

import unittest
from nose.tools import assert_equal
from parameterized import parameterized
import requests
import os
import logging


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

        # logging.basicConfig()

    def test_check_if_base_domain_defined(self):
        logger = logging.getLogger('unittest')
        self.assertIn('DOMAIN',os.environ)
        if 'DOMAIN' in os.environ:
            logger.info("Environment variable DOMAIN is defined.")
            logger.info("DOMAIN="+os.environ['DOMAIN'])
            logger.info("Fetching with headers: " + str(self.headers))

    @parameterized.expand([
        ("/", 200, None, "Home page - Response code failed"),
        ("/desktops", 200, None, "Category page - Response code failed"),
        ("/desktops/mac", 200, None, "Sub-cat page - Response code failed"),
        ("/desktops/mac/imac", 200, None, "PDP - Response code failed"),
        ("/",None,"0s","Home page - cache test failed"),
        ("/desktops", None, "000", "Category page - cache test failed"),
        ("/desktops/mac", None, "000", "Sub-cat page - cache test failed"),
        ("/desktops/mac/imac", None, "000", "PDP - cache test failed")
    ])
    def test_request_status_code(self,url, expected_status_code, expected_ttl, error_message):
        logger = logging.getLogger('unittest')
        if 'DOMAIN' in os.environ:
            self.headers['Host'] = os.environ['DOMAIN']
            url = "http://" + os.environ['DOMAIN'] + ".edgesuite-staging.net" + url
            response = requests.get(url, headers=self.headers)
            logger.debug("Fetching URL: " + url)
            logger.debug("Using headers: " + str(self.headers) )
            logger.debug("Response status: " + str(response.status_code))
            logger.debug("Response headers: " + str(response.headers) )

            if expected_status_code != None:
                assert_equal(response.status_code, expected_status_code, msg=error_message)
            else:
                ttl = response.headers['X-Cache-Key'].split('/')[4]
                assert_equal(expected_ttl, ttl, msg=error_message)


if __name__ == "__main__":
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logging.getLogger('unittest').setLevel(logging.DEBUG)
    unittest.main()
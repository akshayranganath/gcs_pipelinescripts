import unittest
import requests

class RunCheck(unittest.TestCase):

    def setUp(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip/deflate",
            "Connection": "keep-alive",
            "Accept-Language":"en-use",
            "Pragma": "akamai-x-get-cache-key"
        }

    def test_check_resonse(self, test_object_tuple, base_domain):
        (self.url, self.expected_response_code, self.expected_ttl, self.error_message) = test_object_tuple
        response = requests.get('http://' + base_domain + self.url, headers=self.headers)
        if self.expected_response_code!= None and self.expected_response_code!='':
            self.assertEqual(response.status_code, int(self.expected_response_code), msg=self.error_message)
        else:
            #get the ttl
            ttl = response.headers['X-Cache-Key'].split('/')[4]
            self.assertEqual(self.expected_ttl, ttl, msg=self.error_message)

if __name__ == "__main__":
    unittest.main()
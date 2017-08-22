from nose.tools import assert_equal
from parameterized import parameterized
import requests

headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip/deflate",
            "Connection": "keep-alive",
            "Accept-Language":"en-use",
            "Pragma": "akamai-x-get-cache-key"
        }

@parameterized.expand([
    ("/", 200, None, "Home page - Response code failed"),
    ("/men.html", 200, None, "Category page - Response code failed"),
    ("/men/new-arrivals.html", 200, None, "Sub-cat page - Response code failed"),
    ("/men/new-arrivals/linen-blazer.html", 200, None, "PDP - Response code failed"),
    ("/",None,"30d","Home page - cache test failed"),
    ("/men.html", None, "30d", "Category page - cache test failed"),
    ("/men/new-arrivals.html", None, "30d", "Sub-cat page - cache test failed"),
    ("/men/new-arrivals/linen-blazer.html", None, "7d", "PDP - cache test failed")
])
def test_request_status_code(url, expected_status_code, expected_ttl, error_message):
    response = requests.get('http://devopstest.gcs.akamai.com.edgekey-staging.net'+url, headers=headers)
    if expected_status_code != None:
        assert_equal(response.status_code, expected_status_code, msg=error_message)
    else:
        ttl = response.headers['X-Cache-Key'].split('/')[4]
        assert_equal(self.expected_ttl, ttl, msg=error_message)


import os
import requests
from behave import *

@given('I open /sw_worker.js')
def step_connect_to_website(context):
    response = requests.get('https://www.akshayranganath.com/style.css',verify=False)
    assert response.status_code == 200
    context.response = response
    context.headers = response.headers

@when('JS Response is a 200')
def step_check_response_code(context):
    assert context.response.status_code == 200


@then('JS TTL should be 1 day')
def step_check_ttl(context):
    response = context.response
    assert 'True-TTL' in response.headers
    print(response.headers['True-TTL'])
    assert response.headers['True-TTL'] == "86400"

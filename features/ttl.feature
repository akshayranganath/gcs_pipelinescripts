Feature: Check TTL settings
    In order to verify Akamai integration, we need to verify the TTL settings of some common file types.

    Scenario: Check Home Page TTL
        Given   I open the home page
        When    There is no error
        Then    TTL should be -1


    Scenario: Check CSS File TTL
        Given   I open the URL /style.css
        When    Response is a 200
        Then    TTL should be 1 day

    Scenario: Check JS file TTL
        Given   I open /sw_worker.js
        When    JS Response is a 200
        Then    JS TTL should be 1 day
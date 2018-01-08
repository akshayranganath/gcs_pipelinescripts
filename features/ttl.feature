Feature: Check TTL settings
    In order to verify Akamai integration, we need to verify the TTL settings of some common file types.

    Scenario: Check Home Page TTL
        Given   I open the home page
        When    There is no error
        Then    TTL should be -1



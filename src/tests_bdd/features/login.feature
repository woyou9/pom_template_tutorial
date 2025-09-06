Feature: Login

  Scenario: Signing in with correct data
    Given User on login page
    When I enter correct login and password and click "Login"
    Then I see "You logged into a secure area!" text

  Scenario: Signing in with incorrect password
    Given User on login page
    When I enter correct login but incorrect password and click "Login"
    Then I see "Your password is invalid!" text

  Scenario: Signing in with incorrect username
    Given User on login page
    When I enter incorrect login and correct password and click "Login"
    Then I see "Your username is invalid!" text
Feature: Login

  Scenario Outline: Signing in to practice page
    Given User on login page
    When I enter "<login>" as login and "<password>" as password and click "Login"
    Then I see "<message>" text
    Examples: Logins, Passwords, Messages
      | login         | password              | message                        |
      | practice      | SuperSecrectPassword! | You logged into a secure area! |
      | practice      | randomPassw0rd321!    | Your password is invalid!      |
      | wrongusername | randomPassw0rd321!    | Your username is invalid!      |
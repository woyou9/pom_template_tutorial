from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then, parsers
from pages.page_objects.home_page import HomePage
from pages.page_objects.login_page import LoginPage


@scenario('../features/login.feature', 'Signing in with correct data')
def test_login_01():
    pass

@scenario('../features/login.feature', 'Signing in with incorrect password')
def test_login_02():
    pass

@scenario('../features/login.feature', 'Signing in with incorrect username')
def test_login_03():
    pass

@given("User on login page")
def user_on_login_page(login_page: LoginPage):
    pass

@when('I enter correct login and password and click "Login"')
def enter_credentials_and_submit(login_page: LoginPage):
    login_page.accept_cookies()
    login_page.sign_in(username='practicee',
                       password='SuperSecretPassword!')

@then(parsers.parse('I see "{text}" text'))
def assert_message(login_page: LoginPage, text: str):
    print(text)
    expect(login_page.page.get_by_text(text)).to_be_visible()

@then('"Logout" button is visible')
def assert_logout_button(home_page: HomePage):
    expect(home_page.page.locator('a[href="/logout"]')).to_be_visible()

@when('I enter correct login but incorrect password and click "Login"')
def enter_credentials_and_submit(login_page: LoginPage):
    login_page.sign_in(username='practice',
                       password='randomwrongpassw0rd!123')

@when('I enter incorrect login and correct password and click "Login"')
def enter_credentials_and_submit(login_page: LoginPage):
    login_page.sign_in(username='randomwrongusername123',
                       password='SuperSecretPassword!')

import pytest
from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then, parsers
from pages.page_objects.home_page import HomePage
from pages.page_objects.login_page import LoginPage


@pytest.fixture # fixture zwracający pusty słownik - pozwala na dzielenie danych między krokami
def shared_data() -> dict:
    return {}

@scenario('../features/login.feature', 'Signing in with correct data')
def test_login_01() -> None: # pusta funkcja testowa, służy jedynie do powiązania scenariusza z pliku feature
    pass

@scenario('../features/login.feature', 'Signing in with incorrect password')
def test_login_02() -> None:
    pass

@scenario('../features/login.feature', 'Signing in with incorrect username')
def test_login_03() -> None:
    pass

@given('User on login page')
def user_on_login_page(login_page: LoginPage) -> None:
    pass # krok pusty, bo przejście na strone logowania jest w konstruktorze LoginPage - samo utworzenie obiektu przez fixture przejdzie na stronę logowania
    # bez tego tutaj znajdowałoby się coś w stylu login_page.navigate_to_login_page()

@when('I enter correct login and password and click "Login"')
def enter_credentials_and_submit(login_page: LoginPage, shared_data: dict) -> None:
    login_page.accept_cookies()
    with login_page.page.expect_response('https://practice.expandtesting.com/secure') as response_info: # expect_response opisane w src/tests/test_template.py::test_09
        login_page.sign_in(username='practice',
                           password='SuperSecretPassword!')
    shared_data['response_status'] = response_info.value.status # zapisujemy status response'a w słowniku

@when('I enter correct login but incorrect password and click "Login"')
def enter_credentials_and_submit(login_page: LoginPage) -> None:
    login_page.sign_in(username='practice',
                       password='randomwrongpassw0rd!123')

@when('I enter incorrect login and correct password and click "Login"')
def enter_credentials_and_submit(login_page: LoginPage) -> None:
    login_page.sign_in(username='randomwrongusername123',
                       password='SuperSecretPassword!')

@then(parsers.parse('I see "{text}" text and response from /secure is 200'))
def assert_logged_in(login_page: LoginPage, text: str, shared_data: dict) -> None:
    expect(login_page.page.get_by_text(text)).to_be_visible()
    assert shared_data['response_status'] == 200 # wykorzystujemy wartość ze słownika do asercji w kolejnym kroku

@then(parsers.parse('I see "{text}" text'))
def assert_error_message(login_page: LoginPage, text: str) -> None:
    expect(login_page.page.get_by_text(text)).to_be_visible()

@then('"Logout" button is visible')
def assert_logout_button(home_page: HomePage) -> None:
    expect(home_page.page.locator('a[href="/logout"]')).to_be_visible()


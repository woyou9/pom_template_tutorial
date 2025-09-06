from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then, parsers
from pages.page_objects.home_page import HomePage
from pages.page_objects.login_page import LoginPage


@scenario('../features/login_outline.feature', 'Signing in to practice page')
def test_login_outline_01():
    pass


@given('User on login page')
def user_on_login_page(login_page: LoginPage):
    expect(login_page.page.get_by_text('Test Login page for Automation Testing Practice')).to_be_visible()


@when(parsers.parse('I enter "{login}" as login and "{password}" as password and click "Login"'))
def sign_in(login_page: LoginPage, login: str, password: str):
    login_page.sign_in(login, login)


@then(parsers.parse('I see "{text}" text'))
def assert_message(login_page: LoginPage, text: str):
    expect(login_page.page.get_by_text(text)).to_be_visible()
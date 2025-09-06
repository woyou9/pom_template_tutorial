from playwright.sync_api import Page
from pages.locators.login_page_locators import (LoginPageLocators,
                                                LoginPageRoleLocators,
                                                LoginPageTextLocators)


class LoginPage:
    login_page_url = 'https://practice.expandtesting.com/login'
    
    def __init__(self, page: Page):
        self.page = page # rozszerzenie funkcjonalności page'a klasy o metody playwrightowego page (np. .goto(), .click(), .fill() itd.)
        # Przykładowe pola instancji klasy LoginPage i różne sposoby wyszukiwania elementów na stronie. Hardcoded i z użyciem klas locatorów.
        self.login_input_field = self.page.locator(LoginPageLocators.LOGIN_INPUT_FIELD)
        self.password_input_field = self.page.get_by_label('Password')
        self.login_button = self.page.get_by_role(role='button',
                                                  name=LoginPageRoleLocators.LOGIN_BUTTON_NAME)
        self.register_button = self.page.get_by_text(text='Register')
        self.reset_password_button = self.page.get_by_role(role='button').filter(has_text='Reset')
        self.invalid_email_message = self.page.get_by_text(LoginPageTextLocators.INVALID_EMAIL_MESSAGE)
        self.page.goto(self.login_page_url) # utworzenie instancji klasy LoginPage spowoduje przejście do url strony logowania

        # Przykładowa metoda klasy LoginPage odpowiedzialna za logowanie
    def sign_in(self, username: str, password: str) -> None:
        self.login_input_field.clear()
        self.login_input_field.fill(username)
        self.password_input_field.clear()
        self.password_input_field.fill(password)
        self.login_button.click()

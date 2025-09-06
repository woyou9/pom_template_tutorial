from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.logout_button = self.page.locator('.button').filter(has_text='Logout')

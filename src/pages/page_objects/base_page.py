from playwright.sync_api import Page, Locator


# klasa bazowa z której dziedziczą wszystkie pages, można w niej definiować metody pomagające z elementami
# które powtarzają się w całej aplikacji, czyli są tak samo zbudowane na każdej stronie
class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def link_button(self, btn_name: str) -> Locator:
        # przykładowo, przycisk w danej apce czasami jest linkiem <a href="https://"></a>, taka metoda zwróci ten przycisk
        # jeżeli podamy jego tekst jako argument
        return self.page.locator('a').filter(has_text=f'^{btn_name}$')

        # wszystkie te metody są randomowe, w trakcie pisania klas page'ów widać które fragmenty często się
        # powtarza i na podstawie tego można tworzyć takie helpery
    def button(self, btn_name: str) -> Locator:
        return self.page.get_by_role('button', name=btn_name, exact=True)

        # analogicznie można stworzyć helpera który od razu wykonuje konkretną akcje na elemencie, a nie tylko go zwraca
        # np. kliknie button z określonym tekstem
    def click_button(self, btn_name: str) -> None:
        self.page.get_by_role('button', name=btn_name, exact=True).click()

    def textbox_by_label(self, label: str) -> Locator:
        return self.page.get_by_label(label)

    def combobox_options_by_label(self, label: str) -> Locator:
        pass # return

    def select_combobox_option(self, label: str, option_name: str) -> None:
        self.combobox_options_by_label(label).filter(has_text=f'^{option_name}$').click()

    # @property sprawi, że metoda (def side_menu) będzie wyglądać jak pole - self.side_menu, a nie self.side_menu()
    # dodatkowo nie utworzy elementu (w tym wypadku instacji klasy SideMenu) dopóki go nie użyjemy
    @property
    def side_menu(self) -> "SideMenu":
        # definiujemy side_menu w BasePage, wtedy każdy page który po nim dziedziczy będzie mieć dostęp do side_menu
        # gdyby przykładowo menu nie było widoczne we wszystkich miejscach, ten sam fragment kodu zamiast w BasePage
        # wpisalibyśmy w klasach page'y, dla których menu boczne jest widoczne
        return SideMenu(self.page)

    def sign_out(self):
        self.side_menu.sign_out_button.click() # wykorzystanie side_menu do wylogowania się z apki


# w tym samym pliku co BasePage
# reprezentuje np. menu boczne, które jest dostępne w całej apce. Pola klasy reprezentują przyciski na menu bocznym
class SideMenu(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.user_button = self.link_button('User')
        self.settings_button = self.link_button('Settings')
        self.sign_out_button = self.link_button('Sign out')
# analogicznie w aplikacji która ma formularze do wypełnienia, można utworzyć np. klasę FormElements, która zawierałaby
# przyciski powtarzalne dla każdego formularza, np. "Zapisz", "Anuluj" etc. jako pola klasy


# w innym pliku, klasa reprezentująca jakiś page
class SomePage(BasePage): # dziedziczy po BasePage
    def __init__(self, page: Page):
        super().__init__(page) # konstruktor klasy rodzica (BasePage)

    def random_method(self) -> None:
        self.side_menu.settings_button.click() # <- dostęp do side_menu
        self.link_button('tekst na przycisku').click() # <- dostep do metod pomocniczych
        self.button('tekst na przycisku').click()      # <-
import pytest
from pages.page_objects.home_page import HomePage
from utils.logger import logger
from utils.json_data_helper import BROWSER_TYPES, LOGIN_SCENARIOS
from playwright.sync_api import Page, expect
from pages.page_objects.login_page import LoginPage


# Wybierz przeglądarkę jako argument
# pytest --test-browser chrome/firefox/webkit/edge (domyślnie chrome)
# pytest -włączy wszystkie testy
# pytest -k 'example' -włączy testy z keywordem 'example' w nazwie
# pytest folder z testami\plik z testami::nazwa funkcji testowej -włączy tylko konkretny test
    # np. pytest tests\test_template::test_01
# pytest --headless -uruchomi test w trybie headless (nie będą widoczne)


def test_01(page: Page) -> None:
    page.goto(url='https:\\google.com', wait_until='load')
    page.get_by_role(role='button', name='Odrzuć wszystko').click()
    page.wait_for_timeout(5000)
    # otworzy google, odrzuci ciasteczka i poczeka 5 sekund (dla chrome, edge i firefox w full screenie)
    logger.debug('Test DEBUG log.')
    logger.info('Test INFO log.')
    logger.warning('Test WARNING log.')
    logger.error('Test ERROR log.')
    logger.critical('Test CRITICAL log.')
    # powinno wyświetlić w konsoli testowe wiadomości dla każdego poziomu logu i zapisać je do pliku (src/artifacts/playwright_tests.log)
    # kolejność logów wg poziomu (debug najmniejszy, critical największy)


# odpali test raz dla każdej przeglądrki (4 razy - chrome/firefox/webkit/edge), dokładniejszy przykład parametryzacji w test_04
@pytest.mark.parametrize('browser_type', BROWSER_TYPES)
def test_02(page, browser_type) -> None:
    page.goto(url='https:\\google.com', wait_until='load')
    page.get_by_role(role='button', name='Odrzuć wszystko').click()


def test_03(login_page: LoginPage, home_page: HomePage) -> None: # wykorzystanie login_page/home_page fixture żeby utworzyć instancje klasy na potrzeby testu
    login_page.sign_in(username='practice',
                       password='SuperSecretPassword!') # wykorzystanie metody klasy LoginPage

    expect(home_page.page.get_by_text(text='You logged into a secure area!', exact=True)).to_be_visible() # asercja - element z dokładnym tekstem ma być widoczny
    expect(home_page.page.locator('.main-navbar')).to_be_visible() # asercja - element, który reprezentuje locator (główne menu) ma być widoczny

    logger.info(home_page.page.locator('.subheader').text_content()) # info log zawierający tekst jednego z elementów strony

    home_page.page.locator('.navbar-nav').filter(has_text='Test Cases').click() # kliknięcie w element zawierający tekst 'Test Cases' na głównym pasku nawigacji


# przykładowa parametryzacja testu logowania, LOGIN_SCENARIOS to lista w której są 3 słowniki, każdy słownik reprezentuje jeden przypadek testowy
# parametrize wykona test jeden raz dla każdej pozycji iterowalnego elementu który przekażemy w argumencie
# np. @pytest.mark.parametrize('jeden_test', ['element 1', 'element 2', 'element 3', 'element 4']) wykona 4 testy
# analogicznie [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}] też wukona 4 testy, nawet gdyby każdy z tych słowników miał więcej pozycji {"key":"value"}
@pytest.mark.parametrize('test_case', LOGIN_SCENARIOS) # struktura pliku w data/login_scenarios.json
def test_04(login_page: LoginPage, home_page: HomePage, test_case) -> None: # test_case w tym wypadku to jeden słownik
    logger.info(f'Now running test case: {test_case.get("test_case_name")}') # log wyświetlający który przypadek testowy jest obecnie wykonywany

    login_page.sign_in(username=test_case.get('username'),  # ze słownika wyciągana jest wartość dla klucza 'username'
                       password=test_case.get('password'))  # analogicznie dla klucza 'password')

    match test_case.get('test_case_name'): # wyciągana jest nazwa testu
        # match case -> jeżeli nazwa testu (match) = case wykonaj odpowiednie akcje (w tym wypadku asercje)

        case 'valid_login': # dla poprawnego loginu oczekuj widocznego elementu o tekście "You logged into a secure area!"
            expect(home_page.page.get_by_text(text='You logged into a secure area!', exact=True)).to_be_visible()

        case 'invalid_username':  # dla złej nazwy użytkownika oczekuj widocznego elementu o tekście "Your username is invalid!"
            expect(login_page.page.get_by_text(text='Your username is invalid!', exact=True)).to_be_visible()

        case 'invalid_password': # dla złego hasła oczekuj widocznego elementu o tekście "Your password is invalid!"
            expect(login_page.page.get_by_text(text='Your password is invalid!', exact=True)).to_be_visible()


def test_05(logged_in_user: HomePage) -> None: # wykorzystanie fixture logged_in_user, który od razu zaloguje użytkownika i zwróci instancje klasy HomePage
    expect(logged_in_user.logout_button).to_be_visible() # logged_in_user ma dostęp do pól klasy HomePage (logout_button)


# Fixture per function i per session printują do konsoli "Fixture". 
# Test_06 wyprintuje "Fixture" 3 razy, 1 raz na każde wykonanie funkcji testowej (per_function_fixture)
# Test_07 wyprintuje "Fixture" dla całej sesji, czyli tylko raz niezależnie ile jest funkcji testowych (per_session_fixture)
# (scope='function') jest domyślną opcją, czyli pytest.fixture = pytest.fixture(scope='function')
@pytest.mark.parametrize('test', ['1 test', '2 test', '3 test'])
def test_06(per_function_fixture, test) -> None:
    pass


@pytest.mark.parametrize('test', ['1 test', '2 test', '3 test'])
def test_07(per_session_fixture, test) -> None:
    pass


def test_08(page: Page) -> None:
    page.goto('https://practice.expandtesting.com/tables')
    
    for e in page.locator('#table1 th').all(): 
        logger.info(e.text_content()) # text wszystkich nagłówków tabeli

    for e in page.locator('#table1 tr').all(): 
        logger.info(e.text_content()) # text wszystkich wierszy tabeli

    for e in page.locator('#table1 td').all(): 
        logger.info(e.text_content()) # text wszystkich komórek tabeli

    
    col_names = ['First Name', 'Last Name', 'Email']
    
    def get_column_number(column_names: list[str]): # funkcja która zwróci listę numerów kolumn o danych nazwach
        return [page.locator('#table1 thead tr th').all_text_contents().index(name) + 1 for name in column_names]

    for number in get_column_number(col_names):
        for td in page.locator(f'#table1 tr td:nth-of-type({number})').all():
            logger.info(td.text_content()) # text wszystkich komórek dla kolumn z listy col_names


def test_09(login_page: LoginPage) -> None:
    login_page.accept_cookies()
    with login_page.page.expect_response('https://practice.expandtesting.com/secure') as response_info: # ustawia context managera - poczekaj na response z tego URL
        login_page.sign_in(username='practice',
                           password='SuperSecretPassword!') # w środku context managera akcje wywołujące response

    # response_info.value daje dostęp do konkretnych informacji tego response'a
    logger.info(response_info.value.status)
    logger.info(response_info.value.status_text)
    logger.info(response_info.value.request)


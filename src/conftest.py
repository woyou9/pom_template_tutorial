import datetime
from typing import Iterator
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from pages.page_objects.home_page import HomePage
from pages.page_objects.login_page import LoginPage
from utils.database_connection import DatabaseConnection
from utils.json_data_helper import JSONDataHelper


AUTH_DATA: dict = JSONDataHelper('auth_data.json').load()
DATABASE_INFO: dict = JSONDataHelper('database_info.json').load()


def pytest_addoption(parser) -> None:
    parser.addoption(
        '--test-browser',
        action='store',
        default='chrome',
        choices=['chrome', 'firefox', 'webkit', 'edge'],
        help='Select browser to run tests in.'
    ), # parser.addoption() - dodanie opcji do pytest (takiej jak np. -s -v -m itp.), w tym wypadku wybór przeglądarki np. --test-browser firefox
    parser.addoption(
        '--headless',
        action='store_true',
        help='Add to run in headless mode (no GUI)'
    ), # dodanie --headless spowoduje, że test nie będzie widoczny
    parser.addoption(
        '--env',
        action='store',
        default='localhost',
        choices=['localhost', 'preprod', 'prod'],
        help='Choose the environment to run tests in.'
    ) # wybór środowiska, nie ma wpływu na żadne testy w tym projekcie, użyte jedynie w przykładzie dotyczącym bazy danych


# return request.config.getoption(--option)
# zwróci wartość podaną dla konkretnej opcji w terminalu
@pytest.fixture(scope='session')
def test_environment(request):
    return request.config.getoption('--env')


@pytest.fixture(scope='session')
def get_slowmo_value(request) -> int:
    return int(request.config.getoption('--slowmo'))


@pytest.fixture(scope='session')
def is_headless(request) -> bool:
    return request.config.getoption('--headless')


@pytest.fixture(scope='session')
def browser_type(request) -> str:
    return request.config.getoption('--test-browser')


# fixture na połączenie z bazą danych, wykorzystuje klase DatabaseConnection
# przekazuje dane (zależne od opcji --env) z DATABASE_INFO (plik ./data/database_info.json) do konstruktora klasy i tworzy obiekt reprezentujący połączenie z bazą
# klasa DatabaseConnection znajduje się w pliku ./utils/database_connection.py
@pytest.fixture
def database_connection(test_environment):
    db_config: dict = DATABASE_INFO[test_environment]
    db_connection: DatabaseConnection = DatabaseConnection(database_config=db_config)
    yield db_connection
    db_connection.close()


# fixture dla przeglądarki, fixture browser_type zwróci string przekazany do opcji --test_browser i na podstawie tego utworzy odpowiednią przeglądarkę
@pytest.fixture
def browser(browser_type: str, is_headless: bool, get_slowmo_value: int) -> Iterator[Browser]:
    with sync_playwright() as playwright:
        match browser_type:
            case 'chrome':
                browser: Browser = playwright.chromium.launch(headless=is_headless,
                                                              args=['--start-maximized'],
                                                              slow_mo=get_slowmo_value)
            case 'firefox':
                browser: Browser = playwright.firefox.launch(headless=is_headless,
                                                             args=['--kiosk'],
                                                             slow_mo=get_slowmo_value)
            case 'webkit':
                browser: Browser = playwright.webkit.launch(headless=is_headless,
                                                            slow_mo=get_slowmo_value)
            case 'edge':
                browser: Browser = playwright.chromium.launch(headless=is_headless,
                                                              channel='msedge',
                                                              args=['--start-maximized'],
                                                              slow_mo=get_slowmo_value)
        yield browser # zwraca przeglądarkę i zatrzymuje wykonywanie funkcji, po teście wróci tutaj ją zamknać
        browser.close()


# fixture dla contextu przeglądarki, przyjmuje przeglądarkę jako argument
@pytest.fixture
def browser_context(browser: Browser, request) -> Iterator[BrowserContext]:
    context: BrowserContext = browser.new_context(no_viewport=True)
    # tracing pozwala na podgląd przebiegu całego testu ze szczegółami w przeglądarce (playwright show-trace path/to/trace.zip)
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    context.set_default_timeout(15000) # ustawia globalny defaultowy timeout (domyślnie 30000ms)
                                       # można nadpisać globalny timeout dla konkretnych akcji np. self.jakiś_przycisk.click(timeout=5000)

    yield context
    # zwraca context i zatrzymuje wykonywanie funkcji, po teście wróci tutaj go zamknać

    if request.node.rep_call.failed: # zapisujemy trace tylko kiedy test będzie negatywny
        context.tracing.stop(
            path=f'./artifacts/tracing/{request.node.module.__name__}.{request.node.name}_trace_'
                 f'{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip')
                    # nazwa pliku - moduł.nazwa-testu_trace_YYYY-MM-DD_H-M-S.zip
    else:
        context.tracing.stop()

    context.close()


# fixture dla strony, przyjmuje context jako argument
@pytest.fixture
def page(browser_context: BrowserContext) -> Iterator[Page]:
    page: Page = browser_context.new_page()
    yield page
    # zwraca page i zatrzymuje wykonywanie funkcji, po teście wróci tutaj go zamknać
    page.close()


# fixture zwracający pusty słownik - pozwala na dzielenie danych między krokami
@pytest.fixture(scope='module')
def bdd_shared_data() -> dict:
    return {}


# W argumencie funkcji testowej trzeba podać login_page, wtedy zostanie utworzona nowa instancja klasy LoginPage
# na potrzeby tego testu. Nie trzeba będzie tego robić manualnie w teście.
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def logged_in_user(page: Page, login_page: LoginPage) -> HomePage:
    login_page.sign_in(username=AUTH_DATA['standard_user'].get('username'),
                       password=AUTH_DATA['standard_user'].get('password'))
    return HomePage(page)


@pytest.fixture(scope='function') # zobacz tests/test_template/test_06 i test_07
def per_function_fixture() -> None:
    print('Per function fixture')


@pytest.fixture(scope='session') # zobacz tests/test_template/test_06 i test_07
def per_session_fixture() -> None:
    print('Per session fixture')

import datetime
import pytest
from playwright.sync_api import sync_playwright, Page
from pages.page_objects.home_page import HomePage
from pages.page_objects.login_page import LoginPage
from utils.json_data_helper import AUTH_DATA


def pytest_addoption(parser):
    parser.addoption(
        '--test-browser',
        action='store',
        default='chrome',
        choices=['chrome', 'firefox', 'webkit', 'edge'],
        help='Select browser to run tests in.'
    ) # dodanie opcji do pytest (takiej jak np. -s -v -m itp.)


@pytest.fixture(scope='session')
def browser_type(request) -> str:
    return request.config.getoption('--test-browser') # request w czasie testu zobaczy na wartość przekazaną do opcji --test-browser


@pytest.fixture
def browser(browser_type): # fixture dla przeglądarki, fixture browser_type zwróci string przekazany do opcji --test_browser i na podstawie tego utworzy odpowiednią przeglądarkę
    with sync_playwright() as playwright:
        match browser_type:
            case 'chrome':
                browser = playwright.chromium.launch(headless=False, args=['--start-maximized'])
            case 'firefox':
                browser = playwright.firefox.launch(headless=False, args=['--kiosk'])
            case 'webkit':
                browser = playwright.webkit.launch(headless=False)
            case 'edge':
                browser = playwright.chromium.launch(headless=False, channel='msedge', args=['--start-maximized'])
        yield browser # zwraca przeglądarkę i zatrzymuje wykonywanie funkcji, po teście wróci tutaj ją zamknać
        browser.close()


@pytest.fixture
def browser_context(browser, request): # fixture dla contextu przeglądarki, przyjmuje przeglądarkę jako argument
    context = browser.new_context(no_viewport=True)
    context.tracing.start( # tracing pozwala na podgląd przebiegu całego testu ze szczegółami w przeglądarce (playwright show-trace path/to/trace.zip)
        screenshots=True,
        snapshots=True,
        sources=True
    )
    yield context # zwraca context i zatrzymuje wykonywanie funkcji, po teście wróci tutaj go zamknać

    if request.node.rep_call.failed: # zapisujemy trace tylko kiedy test będzie negatywny
        context.tracing.stop(
            path=f'./artifacts/tracing/'
                 f'{request.node.module.__name__}_{request.node.name}_trace_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip')
                    # nazwa pliku moduł_nazwa-testu_trace_YYYY-MM-DD_H-M-S.zip
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture
def page(browser_context): # fixture dla strony, przyjmuje context jako argument
    page = browser_context.new_page()
    yield page # zwraca page i zatrzymuje wykonywanie funkcji, po teście wróci tutaj go zamknać
    page.close()


# W argumencie funkcji testowej trzeba podać login_page, wtedy zostanie utworzona nowa instancja klasy LoginPage
# na potrzeby tego testu. Nie trzeba będzie tego robić manualnie w teście.
@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def logged_in_user(page, login_page: LoginPage) -> HomePage:
    login_page.sign_in(username=AUTH_DATA['standard_user'].get('username'),
                       password=AUTH_DATA['standard_user'].get('password'))
    return HomePage(page)


@pytest.fixture(scope='function') # zobacz tests/test_template/test_06 i test_07
def per_function_fixture():
    print('Fixture')


@pytest.fixture(scope='session') # zobacz tests/test_template/test_06 i test_07
def per_session_fixture():
    print('Fixture')




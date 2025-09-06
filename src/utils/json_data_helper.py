import json
from utils.logger import logger


try:
  with (open('./data/browser_types.json') as browser_types_file,
        open('./data/login_scenarios.json') as login_scenarios_file,
        open('./data/auth_data.json') as auth_data_file):
      BROWSER_TYPES: dict = json.load(browser_types_file)
      LOGIN_SCENARIOS: list[dict] = json.load(login_scenarios_file).get('login_scenarios')
      AUTH_DATA: dict[str, dict] = json.load(auth_data_file)
except FileNotFoundError as e:
  logger.error(f'JSON data file not found. Exception: {e}')
  raise


    # otwiera plik json, można z niego wyciągnąć wartość, w tym wypadku dla konkretnej przeglądarki np.
    # FIREFOX: str = BROWSER_TYPES.get('firefox') zwróci string 'firefox'

    #     Struktura pliku browser_types.json
    #
    # {
    #     "chrome": "chrome",
    #     "firefox": "firefox",
    #     "webkit": "webkit"
    # }
    #
    #     Analogicznie, gdyby plik wyglądał tak:
    # {
    #     browser_types: {
    #     "chrome": "chrome",
    #     "firefox": "firefox",
    #     "webkit": "webkit"
    #     }
    # }
    #     Wyciągnięcie wartości wyglądałoby tak:
    #     FIREFOX = BROWSER_TYPES['browser_types']['firefox] /
    #     FIREFOX = BROWSER_TYPES['browser_types'].get('firefox')
    #
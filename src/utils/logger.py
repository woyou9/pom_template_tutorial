import logging
from rich.logging import RichHandler


logger = logging.getLogger('Logger')
logger.setLevel(logging.DEBUG)


# używana jest biblioteka 'rich', normalnie setup loggera dla cli wygląda trochę inaczej
cli_handler = RichHandler(rich_tracebacks=True, show_time=True, show_level=True, show_path=True, highlighter=None,
                          markup=True, log_time_format='%H:%M:%S', omit_repeated_times=False)
cli_handler.setLevel(logging.DEBUG) # minimalny poziom logów dla cli


file_handler = logging.FileHandler(filename='artifacts/playwright_tests.log', mode='w') # mode='w' nadpisuje plik zamiast do niego dopisywać
file_handler.setLevel(logging.INFO) # minimalny poziom logów dla pliku
file_formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s', # format logu w pliku (data - poziom logu - tekst)
    datefmt='%Y-%m-%d at %H:%M:%S' # format daty dla logu w pliku
)
file_handler.setFormatter(file_formatter)


logger.addHandler(cli_handler)
logger.addHandler(file_handler)

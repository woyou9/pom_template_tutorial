from utils.logger import logger
import json
from pathlib import Path
from typing import Any


class JSONDataHelper:
    """
        Klasa JSONDataHelper obsługuje pliki .json.

        Konstruktor:
            JSONDataHelper(file_name: str, search_root: str | Path = "src")
            - file_name: nazwa pliku JSON do załadowania (np. 'auth_data.json')
            - search_root: opcjonalny katalog, od którego rozpoczyna się szukanie pliku (domyślnie 'src')

        Metody:
            .load(section: str | None = None) -> Any
            - section: opcjonalny klucz (sekcja) do wyciągnięcia z JSON
            - Jeśli nie podamy sekcji, zwraca cały plik jako słownik.

        Przykładowe użycie:
            Zawartość całego pliku:
            full_data = JSONDataHelper('auth_data.json').load()
            full_data zwróci słownik:
            {
                "standard_user": {"username": "...", "password": "..."},
                "admin": {"username": "...", "password": "..."}
            }
            Zawartość konkretnej sekcji:
            standard_user = AUTH_DATA.load('standard_user')
            standard_user zwróci słownik:
            {
                "username": "...", "password": "..."
            }
        """
    def __init__(self, file_name: str, search_root: str | Path = "."):
        self.search_root = Path(search_root)
        self.file_name = file_name

        try:
            matches = list(self.search_root.rglob(file_name))
        except Exception as e:
            logger.error(f'Error searching for file "{file_name}" under "{self.search_root}". Exception: {e}')
            raise

        if not matches:
            logger.error(f'File "{file_name}" not found under "{self.search_root}"')
            raise FileNotFoundError(f'File "{file_name}" not found under "{self.search_root}"')

        if len(matches) > 1:
            logger.error(f'Multiple files named "{file_name}" found under "{self.search_root}": {matches}')
            raise FileExistsError(f'Multiple files named "{file_name}" found under "{self.search_root}": {matches}')

        self.file_path = matches[0]

        if self.file_path.suffix.lower() != ".json":
            logger.error(f'Invalid file extension for "{self.file_path}". Expected a .json file.')
            raise ValueError(f'Invalid file extension for "{self.file_path}". Expected a .json file.')

    def load(self, section: str | None = None) -> Any:
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError as e:
            logger.error(f'Invalid JSON file "{self.file_path}". Exception: {e}')
            raise
        except Exception as e:
            logger.error(f'Error opening or reading file "{self.file_path}": {e}')
            raise

        if section is None:
            return data

        if not isinstance(data, dict):
            logger.error(f'Top-level JSON structure must be an object in "{self.file_path}", got {type(data)}')
            raise ValueError(f'Top-level JSON structure must be an object, got {type(data)}')

        if section not in data:
            logger.error(f'Section "{section}" not found in "{self.file_path}"')
            raise KeyError(f'Section "{section}" not found in {self.file_path}')

        return data[section]

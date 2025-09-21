import psycopg2
from utils.logger import logger


class DatabaseConnection:
    def __init__(self, database_config: dict):
        self.db_name = database_config.get('database_name') # <- na podstawie słownika przekazanego do konstruktora przypisuje wartości z niego do pól klasy
        self.user = database_config.get('user')
        self.password = database_config.get('password')
        self.host = database_config.get('host')
        self.port = database_config.get('port')
        self.connection = None

    def __str__(self):
        return (f'an instance of DatabaseConnection class, connected to "{self.db_name}" database '
                f'at {self.host}:{self.port} as "{self.user}" user.')

    def connect(self) -> None: # <- metoda connect wykorzystuje bibliotekę psycopg2 żeby połączyć się z bazą danych
        if not all([self.db_name, self.user, self.password, self.host, self.port]):
            missing = [
                param for param in
                ['db_name', 'user', 'password', 'host', 'port'] if not getattr(self, param)
            ]
            logger.error(f'Connection failed. Database connection details are incomplete. Missing parameters: {missing}')
            raise ValueError('Incomplete database connection details.')
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            logger.info(f'Successfully connected to the "{self.db_name}" database. Now using {self.__str__()}')
        except Exception:
            logger.error(f'Failed to connect to the "{self.db_name}" database.')
            raise

    def execute_sql(self, sql_query: str, params: tuple = None) -> None | list[tuple]: # <- metoda execute_sql służy do wykonywania zapytań
        if not self.connection:
            raise ConnectionError("Can't execute query, database connection not established.")
        try:
            with self.connection.cursor() as cur:
                cur.execute(sql_query, params)

                if cur.description:
                    results: list[tuple] = cur.fetchall()
                    if not results:
                        logger.info('Query returned no results: %s | Params: %s', sql_query, params)
                    return results

                if sql_query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'MERGE')):
                    self.connection.commit()
                    logger.info('Write query executed successfully: %s | Params: %s', sql_query, params)

                return None

        except Exception as e:
            logger.error('Database query failed: %s | Params: %s | Exception: %r', sql_query, params, e)
            self.connection.rollback()
            raise

    def close(self) -> None: # <- zamknięcie połączenia z bazą
        if self.connection:
            self.connection.close()
            logger.info(f'Connection to "{self.db_name}" database at {self.host}:{self.port} closed.')
        else:
            logger.error("Can't close non existing database connection.")

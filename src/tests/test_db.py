from utils.database_connection import DatabaseConnection


# zapytania w tym teście są do bazy "Northwind"
# można zamienić dane w pliku ./data/database_info.json i wykorzystać inną baze postgres
def test_northwind(database_connection: DatabaseConnection) -> None: # <- wykorzystuje fixture database_connection
    database_connection.connect() # <- połączenie przed wykonywaniem zapytań

    rows: list[tuple] = database_connection.execute_sql('SELECT * FROM customers') # przypisanie wyniku zapytania do 'rows'

    for row in rows:
        print(row) # wypisanie wszystkich rekordów zwróconych przez zapytanie

    database_connection.execute_sql("UPDATE customers "
                                    "SET company_name = 'Very important company' "
                                    "WHERE customer_id = 'ALFKI'")

    database_connection.execute_sql("UPDATE customers "
                                                "SET company_name = 'Very important company' "
                                                "WHERE customer_id = %s", # <- w zapytaniu można podstawiać zmienne jako %s
                                                params=('ALFKI',))

    database_connection.execute_sql("UPDATE customers "
                                                "SET company_name = %s "
                                                "WHERE customer_id = %s ",
                                                params=('Very important company','ALFKI')) # <- można podstawić więcej niż 1 zmienną
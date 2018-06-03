import src.prod_database as prod_database_controller
import os


def apply():
    # Change columns to enum
    file_path = os.path.join("migrations", "00000000_01.sql")
    with open(file_path, "r") as file:
        sql = file.read()
    prod_database_controller.database.execute_sql(sql)

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class DataBase:
    def __init__(
        self, _host: str, _db_name: str, _user: str, _password: str, _port: str
    ) -> None:
        self.db_params = {
            "host": _host,
            "database": _db_name,
            "user": _user,
            "password": _password,
            "port": _port,
        }

    def execute_query_in_database(self, query):
        try:
            connection = psycopg2.connect(**self.db_params)
            print("connect to Database")
            cursor = connection.cursor()
            cursor.execute(query)
            print(f"The query {query} executed")
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except psycopg2.Error as e:
            raise RuntimeError(
                f"The query: {query} doesn't executed because of this error: {e}"
            )


if __name__ == "__main__":
    database = DataBase("localhost", "db2", "odoo", "odoo", 5432)
    file_path = "data.txt"
    executed_queries = []
    success_df = []
    failure_df = []

    with open(file_path, "r") as file:
        for line in file:
            try:
                database.execute_query_in_database(line)
                success_df.append(1)
            except Exception as e:
                failure_df.append(1)
                print(f"Error {e}")
            # print(line.strip())

    print(f"len success_df{len(success_df)} : len failure_df{len(failure_df)}")

    y = np.array([len(success_df), len(failure_df)])

    plt.figure(figsize=(10, 6))
    plt.pie(
        y,
        colors=["green", "red"],
        labels=[
            "{} succeed to execute".format(len(success_df)),
            "{} failed to execute".format(len(failure_df)),
        ],
        autopct="%1.1f%%",
    )
    plt.show()

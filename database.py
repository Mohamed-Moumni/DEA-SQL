from langchain_community.utilities import SQLDatabase
from typing import Dict
import re

class DataBase:
    def __init__(self, url: str) -> None:
        self.db = SQLDatabase.from_uri(url)

    def get_table_names(self):
        return "\n".join(self.db.get_usable_table_names())

    def get_context(self):
        context = self.db.get_context()
        return context["table_info"].split('\n\n\n')

    def get_tables_infos(self, context):
        pattern = r'CREATE TABLE (\w+)\s*\(.*'

        self.tables_infos = {}
        for value in context:
            splitted = value.split('\n\n')
            table, example = splitted[0], splitted[1]
            match = re.match(pattern, table)
            if match:
                self.tables_infos[match.group(1)] = {
                    "table_info":table,
                    "example":example
                }
            else:
                print("Table name not found.")
        return self.tables_infos
            
            

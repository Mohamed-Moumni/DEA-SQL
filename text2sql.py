"""
Module: text_to_sql.py

This module provides a TextToSQL class for converting natural language questions to SQL queries.

Usage:
    Initialize the TextToSQL object with the desired language model and database object.
    Use the `get_tables_related_question()` method to get tables related to a question.

Example:
    from langchain.chains.openai_tools import create_extraction_chain_pydantic
    from langchain_core.pydantic_v1 import BaseModel, Field
    from prompt import get_table_names_prompt
    from typing import List, Dict
    import time

    class Table(BaseModel):
        \"\"\"SQL Table in the Database\"\"\"

        name: str = Field(description="Name of table in SQL database.")

    # Initialize TextToSQL object
    text_to_sql = TextToSQL(_model="your_model", _db="your_database")

    # Get tables related to a question
    question = "What are the orders placed by customer X?"
    tables = text_to_sql.get_tables_related_question(question)
    print(tables)

Attributes:
    model (str): The language model used for natural language processing.
    db: The database object used for retrieving table names.

Methods:
    __init__(self, _model, _db) -> None:
        Initializes the TextToSQL object with the provided language model and database object.

    get_tables_related_question(self, question: str) -> List[str]:
        Retrieves tables related to the provided question using the initialized language model and database object.

"""

from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from prompt import get_table_names_prompt
from typing import List, Dict
import time


class Table(BaseModel):
    """SQL Table in the Database"""

    name: str = Field(description="Name of table in SQL database.")


class TextToSQL:
    def __init__(self, _model, _db) -> None:
        """
        Initializes the TextToSQL object with the provided language model and database object.

        Args:
            _model (str): The language model used for natural language processing.
            _db: The database object used for retrieving table names.
        """
        self.model = _model
        self.db = _db

    def get_tables_related_question(self, question: str) -> List[str]:
        """
        Retrieves tables related to the provided question using the initialized language model and database object.

        Args:
            question (str): The natural language question.

        Returns:
            List[str]: A list of tables related to the question.
        """
        tables: List[str] = []
        table_chain = create_extraction_chain_pydantic(
            Table,
            self.model,
            system_message=get_table_names_prompt(self.db.get_table_names(), question),
        )
        chain_answer = table_chain.invoke({"input": question})
        for i in chain_answer:
            tables.append(i.name)
        return tables

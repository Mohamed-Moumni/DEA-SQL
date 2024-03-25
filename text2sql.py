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
        self.model = _model
        self.db = _db

    def get_tables_related_question(self, question: str):
        tables:List[str] = []
        table_chain = create_extraction_chain_pydantic(
            Table, self.model, system_message=get_table_names_prompt(self.db.get_table_names(), question)
        )
        chain_answer = table_chain.invoke({"input": question})
        for i in chain_answer:
            tables.append(i.name)
        return tables
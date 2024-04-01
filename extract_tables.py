from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from prompt import get_table_names_prompt


class Table(BaseModel):
    """SQL Table in the Database"""

    name: str = Field(description="Name of table in SQL database.")

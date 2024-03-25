from typing import List
from text2sql import TextToSQL
from model import Model
import pandas as pd
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from database import DataBase
from dotenv import load_dotenv

questions_path = "questions.csv"

df = pd.read_csv(questions_path, header=None)

questions: List[str] = df[0].tolist()

if __name__ == "__main__":
    load_dotenv()
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    db = DataBase("postgresql://odoo:odoo@localhost:5432/db2")
    context = db.get_context()
    tables = db.get_tables_infos(context)
    for table in tables:
        print(f"{tables[table]}")
    # file = open("test.txt", "w")
    # file.write(tables)
    # for table in tables:
    # print(f"Table: {table}")
    # text_to_sql = TextToSQL(llm, db)
    # while True:
    #     prompt: str = input("Enter Your Question")
    #     if prompt == "break":
    #         break
    #     ## step 1 get the related tables for the question
    #     print(f"Responses: {text_to_sql.get_tables_related_question(prompt)}")

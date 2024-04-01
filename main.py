from typing import List
from text2sql import TextToSQL
from model import Model
import pandas as pd
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from database import DataBase
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from prompt import (
    QUESTION_LABEL_MULTI,
    EASY_FEW_SHOT,
    JOIN_FEW_SHOT,
    NESTED_FEW_SHOT,
    get_easy_class_prompt,
    get_join_class_prompt,
    get_join_nested_class_prompt,
)
from openai import OpenAI
from termcolor import colored
import time


questions_path = "questions.csv"

df = pd.read_csv(questions_path, header=None)

questions: List[str] = df[0].tolist()


def generate_sql_response(model, query: str, classification_hint: str, table_infos):
    response = ""
    if classification_hint and classification_hint == "NON-JOIN, NON-NESTED":
        response = model.generate_response(
            get_easy_class_prompt(table_infos, query, EASY_FEW_SHOT)
        )
    elif classification_hint and classification_hint == "JOIN, NON-NESTED":
        response = model.generate_response(
            get_join_class_prompt(table_infos, query, JOIN_FEW_SHOT)
        )
    else:
        response = model.generate_response(
            get_join_nested_class_prompt(table_infos, query, NESTED_FEW_SHOT)
        )
    return response


if __name__ == "__main__":
    load_dotenv()
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    db = DataBase("postgresql://odoo:odoo@localhost:5432/db2")
    model = Model("gpt-3.5-turbo-1106")
    text_to_sql = TextToSQL(llm, db)
    data_save = open("data.txt", "a")

    model.setup()

    for prompt in questions:
        print(colored("get related tables of the question: ", "green"))
        related_tables = text_to_sql.get_tables_related_question(prompt)
        context = db.get_context()
        tables = db.get_tables_infos(context)
        related_tables_schema: str = db.get_related_tables_schema(
            related_tables, tables
        )
        user_input = "\ntable info:\n{table_info}\nQ: {query}\nA: ".format(
            table_info=related_tables, query=prompt
        )
        print(colored("get classification of the question: ", "green"))
        response: str = model.generate_response(QUESTION_LABEL_MULTI + user_input)
        time.sleep(20)
        print(colored("get the sql response: ", "green"))

        res = response.split("Label:")
        if len(res) == 2:
            sql_response: str = generate_sql_response(
                model,
                prompt,
                res[1],
                related_tables,
            )
            data_save.write(f"{sql_response}\n")
        time.sleep(20)
        # print(f"Response: {response}")

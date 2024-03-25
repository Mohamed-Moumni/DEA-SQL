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
from prompt import QUESTION_LABEL_MULTI
from openai import OpenAI
from termcolor import colored
import time


questions_path = "questions.csv"

df = pd.read_csv(questions_path, header=None)

questions: List[str] = df[0].tolist()

if __name__ == "__main__":
    load_dotenv()
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    db = DataBase("postgresql://odoo:odoo@localhost:5432/db2")
    text_to_sql = TextToSQL(llm, db)
    data_save = open("data.txt", "a")
    for prompt in questions:
        # prompt: str = input("Enter Your Question")
        # if prompt == "break":
            # break
        ## step 1 get the related tables for the question
        # print(colored("Get tables related questions", 'green'))
        related_tables = text_to_sql.get_tables_related_question(prompt)
        # print(related_tables)
        ## step 2 get the database schema and the examples
        # print(colored("Get Context", 'green'))
        context = db.get_context()
        # print(colored("Get table names", 'green'))
        tables = db.get_tables_infos(context)
        # print(colored("Get related tables schema", 'green'))
        related_tables_schema:str = db.get_related_tables_schema(related_tables, tables)
        # step 3 classify the answer
        client = OpenAI()
        user_input = "\ntable info:\n{table_info}\nQ: {query}\nA: ".format(table_info=related_tables, query=prompt)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": QUESTION_LABEL_MULTI + user_input}],
            stream=False,
        )
        response: str = completion.choices[0].message.content
        res = response.split("Label:")
        if len(res) == 2:
            data_save.write(f"Question: {prompt} --- Label: {res[1]}\n")
        time.sleep(40)
        # print(f"Response: {response}")
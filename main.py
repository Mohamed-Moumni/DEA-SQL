from typing import List
from info_identifier import InfoIdentifier
from model import Model
import pandas as pd

prompt_template = """
Assuming that you are a natural language processing expert and statistician, and a data analyst, please
understand the business requirements and break down the requirements description into statistical
elements. It is required to break down user problems into entities, and the main information in the original
problem cannot be lost.
### Here are some examples:
What is the name of the staff that is in charge of the attraction named ’US museum’?
output: {"entities": ["staff", "the attraction named ’US museum’"], "query": "the name of the staff that is
¨in charge of the attraction named ÜS museum"}

How many heads of the departments are older than 56 ?
output: {"entities": ["age older than 56", "number of heads of the departments"], "query": "Number of department heads over 56 years old"}

List the name, born state and age of the heads of departments ordered by age.
output: {"entities": ["name of the heads of departments", "born state of the heads of departments", "age of the heads of departments", "age"], "query": "List the name, born state and age of the heads of departments ordered by age."}

what is the average, minimum, and maximum age of all singers from Chinese?
output: {"entities": ["Chinese", "age of all singers"], "query": "The average, minimum, and maximum age of all singers from Chinese"}

Return the different descriptions of formulas that has been used in the textboo.
output: {"entities": ["the different descriptions of formulas", "formulas", "used in the textbook"], "query":
"The different descriptions of formulas that has been used in the textbook"}

What are the details of the markets that can be accessed by walk or bus?
output: {"entities": ["the details of the markets", "can be accessed by walk or busk"], "query": "The
details of the markets that can be accessed by walk or bus"}

Show the name of colleges that have at least two players.
output: {"entities": ["the name of colleges", "players"], "query": "The name of colleges that have at least
two players"}

How many gold medals has the club with the most coaches won?
output: {"entities": ["gold medals", "club", "coaches"], "query": "The number of gold medals has the club
with the most coaches won"}

List the nominees that have been nominated more than two musicals.
output: {"entities": ["nominees", "nominees that have been nominated", "musicals"], "query": "The
nominees that have been nominated more than two musicals"}

### Please be sure to follow the following specifications:
1."entities" refers to all entities in the requirements, including all description information in the
requirements.
2.Your output must be output in json format, and only this json needs to be returned. It needs to include all
fields in json. The json format is as follows: {"entities":[entities], "query":"Rewritten question, removing
unnecessary content"}
{query_input}
output:
"""

questions_path = "questions.csv"

df = pd.read_csv(questions_path, header=None)

questions:List[str] = df[0].tolist()

if __name__ == "__main__":
    for quest in questions:
        print(f"Question: {quest}")
    # model:Model = Model("gpt-3.5-turbo",0)
    # info_identifier:InfoIdentifier = InfoIdentifier(model, prompt_template)
    # entities:List[str] = info_identifier.start(questions)
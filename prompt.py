def get_table_names_prompt(table_infos, query):
    prompt: str = f"""
    Table Names: {table_infos}
    User question: {query}
    ### need
    You are a data analyst and Odoo expert. In business, you need to use the above table Names to complete a SQL query
    code to solve user problems. I would like to ask you to first match the table fields, and finally determine the required table and all related field information
    and give some key information for writing SQL.
    Note that all table names must be their original names, and the output of field names must be the original field names in the table.
    ### Please be sure to comply with the following specifications
    1. Required table information: Not all tables may need to be selected, depending on the specific problem.
    1.1. Select the table and related fields based on the user questions, entity information and element
    matching information you have given above;
    1.2. The where statement condition only gives the conditions of the corresponding table;
    1.3. All field names required by SQL under the table must include the fields actually needed under the
    corresponding table. Note that you cannot select fields that are not under the previous table name, and do
    not select all fields. You must include all the fields that are needed for the table;
    2. Multi-table joint fields and conditions need to find out the associated fields and conditions between
    multiple tables from the above table information;
    3. "All fields" must to include all the fields actually used in sql !!! You must include all the fields that are needed for the table;
    4. Think step by step, and finally summarize that your output is only in the given json format:
    Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""
    return prompt


prompt_template = """
Assuming that you are a natural language processing expert and statistician, and a data analyst, please
understand the business requirements and break down the requirements description into statistical
elements. It is required to break down user problems into entities, and the main information in the original
problem cannot be lost.

### Here are some examples:

What is the name of the staff that is in charge of the attraction named ’US museum’?
output: {"entities": ["staff", "the attraction named ’US museum’"], "query": "the name of the staff that is charge of the attraction named ÜS museum"}

How many heads of the departments are older than 56 ?
output: {"entities": ["age older than 56", "number of heads of the departments"], "query": "Number of department heads over 56 years old"}

List the name, born state and age of the heads of departments ordered by age.
output: {"entities": ["name of the heads of departments", "born state of the heads of departments", "age of the heads of departments", "age"], "query": "List the name, born state and age of the heads of departments ordered by age."}

what is the average, minimum, and maximum age of all singers from Chinese?
output: {"entities": ["Chinese", "age of all singers"], "query": "The average, minimum, and maximum age of all singers from Chinese"}

Return the different descriptions of formulas that has been used in the textboo.
output: {"entities": ["the different descriptions of formulas", "formulas", "used in the textbook"], "query":"The different descriptions of formulas that has been used in the textbook"}

What are the details of the markets that can be accessed by walk or bus?
output: {"entities": ["the details of the markets", "can be accessed by walk or busk"], "query": "The details of the markets that can be accessed by walk or bus"}

Show the name of colleges that have at least two players.
output: {"entities": ["the name of colleges", "players"], "query": "The name of colleges that have at least two players"}

How many gold medals has the club with the most coaches won?
output: {"entities": ["gold medals", "club", "coaches"], "query": "The number of gold medals has the club with the most coaches won"}

List the nominees that have been nominated more than two musicals.
output: {"entities": ["nominees", "nominees that have been nominated", "musicals"], "query": "The nominees that have been nominated more than two musicals"}

### Please be sure to follow the following specifications:
1."entities" refers to all entities in the requirements, including all description information in the requirements.
2.Your output must be output in json format, and only this json needs to be returned. It needs to include all fields in json.
The json format is as follows: {"entities":[entities], "query":"Rewritten question, removing unnecessary content"}\n
"""

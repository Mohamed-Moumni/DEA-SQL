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


QUESTION_LABEL_MULTI = "For the given question that requires writing SQL, classify it with two labels. " \
                       "You can choose the first label from NON-JOIN and JOIN and choose the second label from " \
                       "NON-NESTED and NESTED.\n\n" \
                        "### Some table infos and examples\n" \
                          "Q: What are the products that are sold this month?" \
                          """table_info: CREATE TABLE sale_order_line (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  product_uom_qty DECIMAL NOT NULL,
  order_id INTEGER NOT NULL,
  date_order DATE NOT NULL
);

CREATE TABLE product_product (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);
""" \
                          "A: Let’s think step by step. The SQL query for the question 'What are the products that are sold this month?' requires data from the sale_order_line table, specifically columns product_id and product_uom_qty, and it also requires data from the product_product table, specifically the name column. Since we need information from two different tables, we need to join them using the common field product_id in sale_order_line and id in product_product, so we label it as JOIN."\
                          "This query retrieves data based on a single condition (sold this month), without requiring nested queries with (INTERSECT, UNION, EXCEPT, IN, NOT IN), so we label it as NON-NESTED."\
                          "Thus the SQL query can be classified as JOIN, NON-NESTED" \
                          "Label: JOIN, NON-NESTED" \
                            "Q: What are the total sales and revenue for each product category?" \
"""CREATE TABLE sale_order_line (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  product_uom_qty DECIMAL NOT NULL,
  price_unit DECIMAL NOT NULL,
  date_order DATE NOT NULL
);

CREATE TABLE product_category (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE product_product (
  id INTEGER PRIMARY KEY,
  category_id INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL
);
""" \
                          "A: Let’s think step by step. The SQL query for the question 'What are the total sales and revenue for each product category?' requires data from the sale_order_line table, specifically columns product_id, product_uom_qty, and price_unit, and it also requires data from the product_product table, specifically the category_id column. Since we need information from two different tables, we need to join them using the common field product_id in sale_order_line and id in product_product. Additionally, we need to group the data by the category_id to calculate total sales and revenue for each product category. So, we label it as JOIN." \
                          "This query retrieves data based on aggregation (total sales and revenue) for each category, without requiring nested queries with (INTERSECT, UNION, EXCEPT, IN, NOT IN), so we label it as NON-NESTED."\
                          "Thus the SQL query can be classified as JOIN, NON-NESTED"\
                          "Label: JOIN, NON-NESTED"\
                          "Q: What are the total sales and revenue for each product category?" \
"""table_info: CREATE TABLE sale_order_line (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  product_uom_qty DECIMAL NOT NULL,
  price_unit DECIMAL NOT NULL,
  date_order DATE NOT NULL
);

CREATE TABLE product_category (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE product_product (
  id INTEGER PRIMARY KEY,
  category_id INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL
);
""" \
                          "A: Let’s think step by step. The SQL query for the question 'What are the total sales and revenue for each product category?' requires data from the sale_order_line table, specifically columns product_id, product_uom_qty, and price_unit, and it also requires data from the product_product table, specifically the category_id column. Since we need information from two different tables, we need to join them using the common field product_id in sale_order_line and id in product_product. Additionally, we need to group the data by the category_id to calculate total sales and revenue for each product category. So, we label it as JOIN."\
                          "This query retrieves data based on aggregation (total sales and revenue) for each category, without requiring nested queries with (INTERSECT, UNION, EXCEPT, IN, NOT IN), so we label it as NON-NESTED."\
                          "Thus the SQL query can be classified as JOIN, NON-NESTED"\
                           "Label: JOIN, NON-NESTED"\
                        "Q: What are the top-selling products in terms of quantity and revenue for the last month?" \
"""table_info: CREATE TABLE sale_order_line (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  product_uom_qty DECIMAL NOT NULL,
  price_unit DECIMAL NOT NULL,
  date_order DATE NOT NULL
);

CREATE TABLE product_product (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);
""" \
                          "A: Let’s think step by step. The SQL query for the question 'What are the top-selling products in terms of quantity and revenue for the last month?' requires data from the sale_order_line table, specifically columns product_id, product_uom_qty, and price_unit, and it also requires data from the product_product table, specifically the name column. Since we need information from two different tables, we need to join them using the common field product_id in sale_order_line and id in product_product. Additionally, we need to filter the data based on the date_order column to consider only the last month's sales. So, we label it as JOIN."\
                          "This query retrieves data based on aggregation (top-selling products) for the last month, without requiring nested queries with (INTERSECT, UNION, EXCEPT, IN, NOT IN), so we label it as NON-NESTED."\
                          "Thus the SQL query can be classified as JOIN, NON-NESTED"\
                          "Label: JOIN, NON-NESTED"\
                            "Q: What are the total sales for each salesperson?" \
"""table_info: CREATE TABLE sale_order (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  amount_total DECIMAL NOT NULL
);
""" \
                          "A: Let’s think step by step. The SQL query for the question 'What are the total sales for each salesperson?' requires data from the sale_order table, specifically columns user_id and amount_total. Since we need to calculate the total sales for each salesperson, we need to group the data by the user_id column. So, we don’t need a joint condition, and we label it as NON-JOIN."\
                          "This query retrieves data based on aggregation (total sales) for each salesperson, without requiring nested queries with (INTERSECT, UNION, EXCEPT, IN, NOT IN), so we label it as NON-NESTED."\
                          "Thus the SQL query can be classified as NON-JOIN, NON-NESTED"\
                          "Label: NON-JOIN, NON-NESTED"\
                        "Q: What are the products that have been ordered by customers from countries with a population greater than 50 million?" \
"""table_info: CREATE TABLE product_product (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE sale_order_line (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  order_id INTEGER NOT NULL
);

CREATE TABLE sale_order (
  id INTEGER PRIMARY KEY,
  country_id INTEGER NOT NULL
);

CREATE TABLE country_population (
  id INTEGER PRIMARY KEY,
  country_id INTEGER NOT NULL,
  population INTEGER NOT NULL
);
""" \
                          "A: Let’s think step by step. The SQL query for the question 'What are the products that have been ordered by customers from countries with a population greater than 50 million?' requires data from multiple tables. We need to first filter the countries with a population greater than 50 million from the country_population table, then find the sales orders associated with these countries from the sale_order table, and finally retrieve the products ordered in these sales orders from the sale_order_line table and their names from the product_product table. This involves a nested query to filter countries based on population. Therefore, we label it as JOIN, NESTED."\
                          "This query involves a nested query (filtering countries based on population), so we label it as NESTED."\
                          "Thus the SQL query can be classified as JOIN, NESTED"\
                          "Label: JOIN, NESTED"\
                       "### Issues you should be concerned about:" \
                        "\ntable info:\n{table_info}\n" \
                        "Q: {query}" \
                        "A: "
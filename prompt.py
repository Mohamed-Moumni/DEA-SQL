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
                          "Label: JOIN, NESTED"


EASY_FEW_SHOT = """
"A: "list users?"\
"Q:SELECT   company_id,   partner_id,   active,   create_date,   login,   password FROM res_users;" \

"A: How many sales orders have been canceled ?"\
"Q: SELECT   COUNT(*) FROM sale_order WHERE   state = 'cancel';" \

"A: How can I retrieve the total sales amount for a customer of id 2?"\
"Q: SELECT SUM(amount_total) AS total_sales_amount FROM sale_orderWHERE partner_id = '2';" \

"A: What is the average order value for each salesperson?"\
"Q: SELECT user_id, AVG(amount_total) AS average_order_value FROM sale_order GROUP BY user_id;" \

"A: What is the total revenue generated in the current month?"\
"Q: SELECT SUM(amount_total) AS total_revenue FROM sale_order WHERE EXTRACT(MONTH FROM date_order) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_order) = EXTRACT(YEAR FROM CURRENT_DATE);" \
"""

JOIN_FEW_SHOT = """
"A: Can I get a list of orders along with their corresponding customer names?"\
"Q: SELECT so.name AS order_number, res.partner.name AS customer_name FROM sale_order AS so JOIN res_partner ON so.partner_id = res_partner.id;" \

"A: What are the total sales amounts for each customer along with their names?"\
"Q: SELECT res_partner.name AS customer_name, SUM(sale_order.amount_total) AS total_sales_amount FROM sale_order JOIN res_partner ON sale_order.partner_id = res_partner.id GROUP BY res_partner.name;" \

"A: Can I retrieve a list of orders placed by each salesperson along with their names?"\
"Q: SELECT sale_order.name AS order_number, res_users.name AS salesperson_name FROM sale_order JOIN res_users ON sale_order.user_id = res_users.id;" \

"A: Can I get a list of orders placed by customers belonging to a specific country along with their country names?"\
"Q: SELECT sale_order.name AS order_number, res_country.name AS country_name FROM sale_order JOIN res_partner ON sale_order.partner_id = res_partner.id JOIN res_country ON res_partner.country_id = res_country.id WHERE res_country.name = 'specific_country_name';" \

"A: give me the details of each product along with their category names?"\
"Q: SELECT product_template.name AS product_name, product_category.name AS category_name FROM product_template JOIN product_category ON product_template.categ_id = product_category.id;" \
"""

NESTED_FEW_SHOT = """
"A: Can I get a list of orders along with their corresponding customer names and the total number of products ordered?"\
"Q: SELECT so.name AS order_number, res_partner.name AS customer_name, (SELECT SUM(sol.product_uom_qty) FROM sale_order_line sol WHERE sol.order_id = so.id) AS total_products_ordered FROM sale_order AS so JOIN res_partner ON so.partner_id = res_partner.id;" \

"A: How can I see the details of each product in an order, including their names, quantities, and the total amount of each order?"\
"Q: SELECT sol.order_id AS order_number, p.name AS product_name, sol.product_uom_qty AS quantity, (SELECT SUM(sol_inner.price_subtotal) FROM sale_order_line sol_inner WHERE sol_inner.order_id = sol.order_id) AS total_order_amount FROM sale_order_line AS sol JOIN product_product AS p ON sol.product_id = p.id;" \

"A: Can I retrieve a list of orders placed by each salesperson along with their names and the total revenue generated by each salesperson?"\
"Q: SELECT res_users.name AS salesperson_name, (SELECT SUM(sale_order_inner.amount_total) FROM sale_order sale_order_inner WHERE sale_order_inner.user_id = res_users.id) AS total_revenue, COUNT(sale_order.id) AS total_orders FROM sale_order JOIN res_users ON sale_order.user_id = res_users.id GROUP BY res_users.name;" \

"A: How can I see the details of each product along with their category names and the total revenue generated from each category?"\
"Q: SELECT product_template.name AS product_name, product_category.name AS category_name, (SELECT SUM(sol_inner.price_subtotal) FROM sale_order_line sol_inner JOIN product_product pp_inner ON sol_inner.product_id = pp_inner.id JOIN product_template pt_inner ON pp_inner.product_tmpl_id = pt_inner.id WHERE pt_inner.categ_id = product_category.id) AS total_category_revenue FROM product_template JOIN product_category ON product_template.categ_id = product_category.id;" \

"A: Can I get a list of orders placed by customers belonging to a specific country along with their country names and the total revenue generated from each country?"\
"Q: SELECT sale_order.name AS order_number, res_country.name AS country_name, (SELECT SUM(sale_order_inner.amount_total) FROM sale_order sale_order_inner JOIN res_partner res_partner_inner ON sale_order_inner.partner_id = res_partner_inner.id WHERE res_partner_inner.country_id = res_country.id) AS total_country_revenue FROM sale_order JOIN res_partner ON sale_order.partner_id = res_partner.id JOIN res_country ON res_partner.country_id = res_country.id;" \
"""

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

def get_easy_class_prompt(table_info, query, few_shots):
  prompt = f"""
  {few_shots}
  ### Database scheme: {table_info}
  ### Please think carefully about the related fields, then write
  valid SQL to solve the following questions based on the above table information, and do not select extra
  columns that are not explicitly requested in the query.
  ### Query: {query}
  ### specification
  1.In sql, just select columns that are explicitly requested in the query.
  2.The output format must strictly meet the following: "SELECT * FROM res_user;"
  """
  return prompt

def get_join_class_prompt(table_info, query, few_shots):
  prompt = f"""
  {few_shots}
  ### Database scheme: {table_info}
  ### Please think carefully about the related fields, then write
  valid SQL to solve the following questions based on the above table information, and do not select extra
  columns that are not explicitly requested in the query.
  ### Query: {query}
  ### HINT: The question may need connection operation like JOIN.
  ### specification
    1."LIMIT" just is used when explicitly requesting how much to retrieve in the query.
    2.In sql, just select columns that are explicitly requested in the query.
    3.The output format must strictly meet the following: "SELECT * FROM res_user;"
  """
  return prompt

def get_join_nested_class_prompt(table_info, query, few_shots):
  prompt = f"""
  {few_shots}
    ### Database scheme:
    {table_info}
    ### Please think carefully about the related fields, then write
    valid SQL to solve the following questions based on the above table information, and do not select extra
    columns that are not explicitly requested in the query.
    ### Query: {query}
    ### HINT: The question may needs nested queries like INTERSECT, UNION, EXCEPT, NOT IN.
    ### specification
    1."LIMIT" just is used when explicitly requesting how much to retrieve in the query.
    2.Don’t use "IN", "OR", "LEFT JOIN" in sql because they aren’t supported in execution engine, you can
    use "INTERSECT" or "EXCEPT" instead.
    3.In sql, just select columns that are explicitly requested in the query.
    4.The output format must strictly meet the following: "SELECT * FROM res_user;"
  """
  return prompt
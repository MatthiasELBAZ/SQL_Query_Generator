import SQLGenerator

if __name__ == '__main__':

    openai_api_key = 'openai_api_key'

    # Set Database URLs
    db_url_dict = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': 'root',
        'password': urllib.parse.quote_plus('mysql'),
        'host': 'localhost',
        'port': '3306',
        'database': 'classicmodels'
    }

    # Create SQLGenerator object
    sql_generator = SQLGenerator(db_url_dict, openai_api_key)

    # Create SQL Prompt
    prompt = "Generate the SQL query to show the postal codes of the last 25 orders grouped by the quantity ordered, in the following database"
    # Generate SQL Query
    schema = sql_generator.generate_db_schema(save=True, json_path='schema.json')
    query = sql_generator.generate_sql_query(prompt, 'text-davinci-003', schema, json_path=None)
    print(query)
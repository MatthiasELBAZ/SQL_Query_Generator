# SQL_Query_Generator

One of my client has different databases and want a tool to be able to:
1. Connect to any of his databases
2. Generate the graph of a database
3. Generate the schema in json file of a database
4. Integrate GPT to generate from a prompt a SQL Query.

I created a class that allows him to fulfill the objectives. The clinet needs as inputs:
1. OpenAi API key
2. The database URL
3. A prompt for GPT to explain the query wanted

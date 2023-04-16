from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph
import json
import openai
import urllib.parse


class SQLGenerator:

    def __init__(self, db_url_dict, openai_api_key):
        self.db_url_dict = db_url_dict
        self.openai_api_key = openai_api_key

    @staticmethod
    def load_json(json_path):
        with open(json_path) as f:
            schema = json.load(f)
        return schema

    @staticmethod
    def write_json(json_data, json_path):
        with open(json_path, 'w') as f:
            f.write(json_data)

    def generate_db_url(self):
        db_url = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'.format(**self.db_url_dict)
        return db_url

    def generate_engine(self):
        engine = create_engine(self.generate_db_url())
        return engine

    def generate_db_metadata(self):
        metadata = MetaData(bind=self.generate_engine())
        metadata.reflect()
        return metadata

    def generate_db_graph(self, save=False, save_path=None):
        metadata = self.generate_db_metadata()
        graph = create_schema_graph(
            metadata=metadata,
            show_datatypes=False,
            show_indexes=False,
            rankdir='LR',
        )
        if save:
            graph.write_png(save_path)
        return graph

    def generate_db_schema(self, save=False, json_path=None):
        metadata = self.generate_db_metadata()
        schema_dict = {}
        for table in metadata.sorted_tables:
            table_dict = {}
            for column in table.columns:
                column_dict = {}
                column_dict['type'] = str(column.type)
                if column.foreign_keys:
                    fk = list(column.foreign_keys)[0]
                    column_dict['references'] = {
                        'table': fk.column.table.name,
                        'column': fk.column.name
                    }
                table_dict[column.name] = column_dict
            schema_dict[table.name] = table_dict
        if save:
            self.write_json(json.dumps(schema_dict), json_path)
        return schema_dict

    def generate_sql_prompt(self, prompt, schema=None, json_path=None):
        if schema is None:
            schema = self.load_json(json_path)
        sql_prompt = f"{prompt}\n\n{json.dumps(schema)}"
        return sql_prompt

    def generate_sql_query(self, prompt, engine, schema=None, json_path=None):
        sql_prompt = self.generate_sql_prompt(prompt, schema, json_path)
        openai.api_key = self.openai_api_key
        response = openai.Completion.create(
            engine=engine,
            prompt=sql_prompt,
            temperature=0.2,
            max_tokens=256,
            best_of=5
        )
        query = response['choices'][0]['text']
        return query




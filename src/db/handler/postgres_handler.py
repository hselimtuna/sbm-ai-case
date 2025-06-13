import pandas as pd
from src.db.conncector.postgres_connector import PostgresConnector


class PostgresHandler:
    def __init__(self):
        self._connector = PostgresConnector()

    def read_data(self, sql_query: str) -> pd.DataFrame:
        df = pd.read_sql(sql=sql_query, con=self._connector.get_engine())
        return df

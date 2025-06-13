from src.db.handler.postgres_handler import PostgresHandler
from typing import Dict, Any, List
from src.utils.query_reader import QueryReader
import os


class ProductDetailExtractor:
    def __init__(self):
        self._db_handler = PostgresHandler()
        self._query_reader = QueryReader()
        self._sql_path = (
            os.getcwd().replace("/extract", "") + "/static/product_detail_info.sql"
        )

    def extract_product_detail(self, product_name: str) -> List[Dict[str, Any]]:
        query = self._query_reader.read_query(
            self._sql_path,
            interpolation=True,
            interpolation_dict={"product_name": product_name},
        )
        df = self._db_handler.read_data(query)
        return df.to_dict(orient="records")

from src.db.handler.postgres_handler import PostgresHandler
from typing import Dict, Any, List
from src.utils.query_reader import QueryReader
from pathlib import Path


class ProductDetailExtractor:
    def __init__(self):
        self._db_handler = PostgresHandler()
        self._query_reader = QueryReader()
        self._path = str(Path.cwd()) + '/src'
        self._sql_path_summary = (
            self._path + "/static/product_detail_info.sql"
        )
        self._sql_path_products = (
            self._path + "/static/products.sql"
        )

    def extract_product_detail(self, product_name: str) -> List[Dict[str, Any]]:
        df = self._db_handler.read_data(
            self._query_reader.read_query(
                self._sql_path_summary,
                interpolation=True,
                interpolation_dict={"product_name": product_name.lower()},
            )
        )
        return df.to_dict(orient="records")

    def extract_unique_products(self) -> List[str]:
        df = self._db_handler.read_data(
            self._query_reader.read_query(self._sql_path_products, interpolation=False)
        )
        return df["name"].to_list()

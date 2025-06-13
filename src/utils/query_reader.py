from typing import Optional


class QueryReader:
    @staticmethod
    def read_query(
        query_path: str, interpolation=False, interpolation_dict=None
    ) -> Optional[str]:
        try:
            with open(query_path) as f:
                query = f.read()
            if interpolation:
                query = query.format(**interpolation_dict)
            return query
        except FileNotFoundError:
            print("path'de dosya yok")

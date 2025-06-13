from config.base_config import conf
from sqlalchemy import create_engine


class PostgresConnector:
    def __init__(self):
        self._db_conf = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
            **conf["DB"]
        )

    def get_engine(self):
        try:
            return create_engine(self._db_conf)
        except Exception as e:
            print("couldnt create the engine")

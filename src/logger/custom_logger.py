import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from threading import Lock
from src.db.conncector.postgres_connector import PostgresConnector
import json

class SingletonLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls, engine=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self._engine = PostgresConnector().get_engine()
        self._logger = logging.getLogger("CustomLogger")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    @classmethod
    def get_logger(cls, engine=None):
        return cls(engine)._logger

    def log_ai_event(self, user_prompt: str, tokens_used: int, model_response: str, query: str):
        msg = f"AI Event | Tokens: {tokens_used} | Response: {model_response} | Query: {query}"
        self._logger.info(msg)

        if not self._engine:
            self._logger.warning("No DB engine provided. Skipping DB insert for AI event.")
            return

        insert_stmt = text("""
            INSERT INTO events_ai (user_prompt, tokens_used, model_response, query)
            VALUES (:user_prompt, :tokens_used, :model_response, :query)
        """)
        try:
            with self._engine.connect() as conn:
                conn.execute(insert_stmt, {
                    "user_prompt": user_prompt,
                    "tokens_used": tokens_used,
                    "model_response": model_response,
                    "query": query
                })
                conn.commit()
        except SQLAlchemyError as e:
            self._logger.error(f"Failed to insert AI event to DB: {e}")

    def log_api_event(self, endpoint: str, method: str, status_code: int, request_payload: dict = None,
                      response_payload: dict = None):
        msg = f"API Event | Endpoint: {endpoint} | Method: {method} | Status: {status_code} | Request: {request_payload} | Response: {response_payload}"
        self._logger.info(msg)

        if not self._engine:
            self._logger.warning("No DB engine provided. Skipping DB insert for API event.")
            return
        insert_stmt = text("""
            INSERT INTO events_api (endpoint, method, status_code, request_payload, response_payload)
            VALUES (:endpoint, :method, :status_code, :request_payload, :response_payload)
        """)
        request_json = json.dumps(request_payload) if request_payload else None
        response_json = json.dumps(response_payload) if response_payload else None

        try:
            with self._engine.begin() as conn:
                conn.execute(insert_stmt, {
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": status_code,
                    "request_payload": request_json,
                    "response_payload": response_json,
                })
        except SQLAlchemyError as e:
            self._logger.error(f"Failed to insert API event to DB: {e}")
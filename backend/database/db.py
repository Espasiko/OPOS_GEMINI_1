import os
import logging
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool

logger = logging.getLogger(__name__)

class Database:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        if cls._connection_pool is None:
            try:
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    1,  # minconn
                    20, # maxconn
                    host=os.getenv("POSTGRES_HOST", "localhost"),
                    port=os.getenv("POSTGRES_PORT", "5432"),
                    database=os.getenv("POSTGRES_DB", "opositaia"),
                    user=os.getenv("POSTGRES_USER", "postgres"),
                    password=os.getenv("POSTGRES_PASSWORD", "postgres")
                )
                logger.info("✅ Database connection pool created")
            except Exception as e:
                logger.error(f"❌ Error creating connection pool: {e}")
                raise

    @classmethod
    def close(cls):
        if cls._connection_pool:
            cls._connection_pool.closeall()
            cls._connection_pool = None
            logger.info("Database connection pool closed")

    @classmethod
    @contextmanager
    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize()
        
        conn = cls._connection_pool.getconn()
        try:
            yield conn
        finally:
            cls._connection_pool.putconn(conn)

    @classmethod
    @contextmanager
    def get_cursor(cls):
        with cls.get_connection() as conn:
            with conn.cursor() as cursor:
                yield cursor
                conn.commit()

# Global instance not needed as we use class methods, but for consistency
db = Database

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=os.getenv('FSTR_DB_HOST', 'localhost'),
                port=os.getenv('FSTR_DB_PORT', '5432'),
                dbname=os.getenv('FSTR_DB_NAME', 'fstr_db'),
                user=os.getenv('FSTR_DB_LOGIN', 'postgres'),
                password=os.getenv('FSTR_DB_PASS', 'postgres'),
                connect_timeout=5
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Error creating connection pool: {str(e)}")
            raise

    @classmethod
    @contextmanager
    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize()

        conn = cls._connection_pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            cls._connection_pool.putconn(conn)

    @classmethod
    @contextmanager
    def get_cursor(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            except Exception as e:
                logger.error(f"Cursor error: {str(e)}")
                raise
            finally:
                cursor.close()


# Инициализация при импорте
try:
    Database.initialize()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
import psycopg
from psycopg_pool import ConnectionPool
from app.core.config import settings
pool = ConnectionPool(
    settings.database_url,
    min_size=1,
    max_size=10,
    open=False,
)
def init_pool():
    pool.open()
    pool.wait()
def get_connection():
    return pool.connection()
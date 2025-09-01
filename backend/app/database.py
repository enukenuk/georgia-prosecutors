from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import logging
from .config import settings

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://testuser:testpassword@localhost:5432/postgres")

logger.info(f"Connecting to database: {DATABASE_URL.replace(DATABASE_URL.split('@')[0].split('://')[1], '***')}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def wait_for_db():
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info("Database connection successful!")

                result = connection.execute(text("""
                                                 SELECT table_name
                                                 FROM information_schema.tables
                                                 WHERE table_schema = 'public'
                                                 """))
                tables = [row[0] for row in result]
                logger.info(f"Found tables: {tables}")

                if 'people' not in tables:
                    logger.warning("Required tables not found! Database may not be initialized.")
                    raise Exception("Tables not found")

                return True

        except Exception as e:
            retry_count += 1
            logger.warning(f"Database connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count >= max_retries:
                logger.error("Failed to connect to database after maximum retries")
                raise
            time.sleep(2)

    return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ != "__main__":
    wait_for_db()
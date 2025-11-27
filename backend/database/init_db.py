"""
Initialize PostgreSQL Database
Runs schema.sql to create tables, views, functions, and triggers
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Create database connection from environment variables
    """
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "opositaia"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )


def create_database_if_not_exists():
    """
    Create database if it doesn't exist
    """
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database="postgres",
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        db_name = os.getenv("POSTGRES_DB", "opositaia")
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            logger.info(f"Creating database: {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"✅ Database {db_name} created")
        else:
            logger.info(f"Database {db_name} already exists")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


def run_schema():
    """
    Run schema.sql to create tables, views, functions, and triggers
    """
    try:
        # Read schema.sql
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        
        if not os.path.exists(schema_path):
            logger.error(f"schema.sql not found at {schema_path}")
            sys.exit(1)
        
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        logger.info("Running schema.sql...")
        
        # Execute schema
        cursor.execute(schema_sql)
        conn.commit()
        
        logger.info("✅ Schema created successfully")
        
        # Verify tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        logger.info(f"Created {len(tables)} tables:")
        for table in tables:
            logger.info(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error running schema: {e}")
        raise


def main():
    """
    Main initialization function
    """
    logger.info("🚀 Initializing OpositAIA Database...")
    
    try:
        # Step 1: Create database if not exists
        create_database_if_not_exists()
        
        # Step 2: Run schema
        run_schema()
        
        logger.info("✅ Database initialization complete!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

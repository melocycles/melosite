import os
import psycopg2
from psycopg2 import pool
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_connection():
    """Get a database connection using the same logic as in sqlCRUD.py"""
    database_url = os.environ.get("DATABASE_URL", "postgres://postgres:mdp@localhost/melodb")

    try:
        # In Docker environment, use the DATABASE_URL environment variable
        if "DATABASE_URL" in os.environ:
            return psycopg2.connect(database_url)
        # Fallback to local connection
        else:
            return psycopg2.connect(host="localhost", database="melodb", user="postgres", password="mdp")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        # Try with sslmode as a last resort
        return psycopg2.connect(database_url, sslmode='require')

def add_indexes():
    """Add indexes to frequently queried columns in the picture table"""
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Add index on bike_id (used in filtering pictures by bike)
        logger.info("Adding index on bike_id column...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_picture_bike_id ON picture(bike_id);
        """)
        
        # Add index on is_principal (used in filtering for principal pictures)
        logger.info("Adding index on is_principal column...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_picture_is_principal ON picture(is_principal);
        """)
        
        # Add composite index on bike_id and is_principal (used together in get_principal_picture_by_bike)
        logger.info("Adding composite index on bike_id and is_principal columns...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_picture_bike_principal ON picture(bike_id, is_principal);
        """)
        
        # Commit the changes
        connection.commit()
        logger.info("All indexes created successfully")
        
    except Exception as e:
        connection.rollback()
        logger.error(f"Error creating indexes: {e}")
    finally:
        cursor.close()
        connection.close()

def analyze_tables():
    """Run ANALYZE on tables to update statistics for the query planner"""
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        logger.info("Running ANALYZE on picture table...")
        cursor.execute("ANALYZE picture;")
        
        connection.commit()
        logger.info("ANALYZE completed successfully")
        
    except Exception as e:
        connection.rollback()
        logger.error(f"Error running ANALYZE: {e}")
    finally:
        cursor.close()
        connection.close()

def optimize_picture_table():
    """Main function to optimize the picture table"""
    logger.info("Starting picture table optimization...")
    
    # Add indexes to frequently queried columns
    add_indexes()
    
    # Update statistics for the query planner
    analyze_tables()
    
    logger.info("Picture table optimization completed")

if __name__ == "__main__":
    optimize_picture_table()
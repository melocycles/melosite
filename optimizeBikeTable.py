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
    """Add indexes to frequently queried columns in the bike table"""
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Add index on dateentre (used in ORDER BY)
        logger.info("Adding index on dateentre column...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_dateentre ON bike(dateentre);
        """)
        
        # Add index on datesortie (used in range queries)
        logger.info("Adding index on datesortie column...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_datesortie ON bike(datesortie);
        """)
        
        # Add index on statutVelo (used in equality filters)
        logger.info("Adding index on statutVelo column...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_statutvelo ON bike(statutvelo);
        """)
        
        # Add indexes on columns used for filtering
        logger.info("Adding indexes on filter columns...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_marque ON bike(marque);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_typevelo ON bike(typevelo);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_tailleRoue ON bike(tailleRoue);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_tailleCadre ON bike(tailleCadre);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bike_etatVelo ON bike(etatVelo);
        """)
        
        # Add index on bikeID in the Modification table
        logger.info("Adding index on bikeID in Modification table...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_modification_bike_id ON modification(bike_id);
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
        logger.info("Running ANALYZE on bike table...")
        cursor.execute("ANALYZE bike;")
        
        logger.info("Running ANALYZE on modification table...")
        cursor.execute("ANALYZE modification;")
        
        connection.commit()
        logger.info("ANALYZE completed successfully")
        
    except Exception as e:
        connection.rollback()
        logger.error(f"Error running ANALYZE: {e}")
    finally:
        cursor.close()
        connection.close()

def optimize_bike_table():
    """Main function to optimize the bike table"""
    logger.info("Starting bike table optimization...")
    
    # Add indexes to frequently queried columns
    add_indexes()
    
    # Update statistics for the query planner
    analyze_tables()
    
    logger.info("Bike table optimization completed")

if __name__ == "__main__":
    optimize_bike_table()
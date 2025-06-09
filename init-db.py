import os
import time
import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_db():
    """Wait for the database to be available"""
    max_retries = 30
    retry_interval = 2  # seconds

    database_url = os.environ.get("DATABASE_URL", "postgres://postgres:mdp@localhost/melodb")

    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting to connect to database (attempt {attempt+1}/{max_retries})...")
            conn = psycopg2.connect(database_url)
            conn.close()
            logging.info("Database connection successful!")
            return True
        except Exception as e:
            logging.warning(f"Database connection failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)

    logging.error("Failed to connect to the database after multiple attempts")
    return False

def create_tables():
    """Create the necessary tables in the database"""
    database_url = os.environ.get("DATABASE_URL", "postgres://postgres:mdp@localhost/melodb")

    try:
        # Connect to the database
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()

        # Create Member table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Member
                       (id SERIAL PRIMARY KEY NOT NULL,
                        username VARCHAR(30) UNIQUE NOT NULL,
                        password CHAR(64) NOT NULL,
                        role VARCHAR(6) NOT NULL,
                        uuid CHAR(36) NOT NULL
                       )''')

        # Create Bike table with column names matching sqlCRUD.py
        cursor.execute('''CREATE TABLE IF NOT EXISTS Bike (
                        id SERIAL PRIMARY KEY NOT NULL,
                        bicycode VARCHAR(12),
                        dateentre DATE NOT NULL,
                        datesortie DATE,
                        marque VARCHAR(20),
                        typeVelo VARCHAR(20),
                        tailleRoue VARCHAR(15),
                        tailleCadre VARCHAR(6),
                        electrique BOOLEAN,
                        origine VARCHAR(11) NOT NULL,
                        statutVelo VARCHAR(17) NOT NULL,
                        etatVelo VARCHAR(11),
                        prochaineAction VARCHAR(10),
                        referent VARCHAR(30),
                        valeur INT,
                        destinataireVelo TEXT,
                        descriptionPublic TEXT,
                        descriptionPrive TEXT,
                        title VARCHAR(25)
                    )''')

        # Create Picture table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Picture(
                       id SERIAL PRIMARY KEY NOT NULL,
                       bike_id INTEGER NOT NULL,
                       name VARCHAR(70) NOT NULL,
                       is_principal BOOL NOT NULL,
                       data BYTEA
                       )''')

        # Create Modification table with JSONB array for suiviModifJSON
        cursor.execute('''CREATE TABLE IF NOT EXISTS Modification(
                       id SERIAL PRIMARY KEY NOT NULL,
                       bike_id INTEGER NOT NULL,
                       suiviModifJSON JSONB[]
                       )''')

        # Create member row
        cursor.execute('''INSERT INTO Member (username, password, role, uuid)
                       VALUES ('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'admin', '6674e3b5-4c24-447f-8b3a-8ddd9c8008e5')
                       ON CONFLICT (username) DO NOTHING''')

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()

        logging.info("Database tables created successfully")
        return True
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    if wait_for_db():
        create_tables()
    else:
        logging.error("Could not initialize the database")

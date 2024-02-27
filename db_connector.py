import os
import psycopg2
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()
# Get database connection variables from environment variables
dbname = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")

# Connect to your PostgreSQL database
try:
    print(dbname)
    print(user)
    print(password)
    print(host)
    print(port)
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    print("Connected to PostgreSQL server")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL server: {e}")

# Define your SQL statement for insertion
def insert_record(job_reference, hospital, position, department, duration, deadline, contact, link):
    # Create a cursor object
    conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
    )       
    cur = conn.cursor()
    
    sql = """INSERT INTO medicalrecruiter.recuiter_job_data(job_reference, hospital, position, department, duration, deadline, contact, link)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    # Define the data you want to insert
    data = (job_reference, hospital, position, department,
                   duration, deadline, contact, link)

    try:
         cur.execute(sql, data)
        # Commit the transaction
         
         conn.commit()
    except (Exception, psycopg2.Error) as error:
     logging.error(f"Error inserting record: {error}")
    finally:
        if conn:
         cur.close()
         conn.close()
         logging.info("PostgreSQL connection is closed")



    # Close the cursor
    cur.close()

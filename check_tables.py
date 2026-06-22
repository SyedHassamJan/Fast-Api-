import psycopg2
from app.config.app_config import getAppConfig

config = getAppConfig()
conn = psycopg2.connect(config.database_url)
cursor = conn.cursor()

# Check all tables in the database
cursor.execute("""
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_type='BASE TABLE'
    ORDER BY table_schema, table_name;
""")

print("Tables in database:")
for schema, table in cursor.fetchall():
    print(f"  {schema}.{table}")

conn.close()

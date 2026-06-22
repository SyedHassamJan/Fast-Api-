import psycopg2
from app.config.app_config import getAppConfig

config = getAppConfig()
conn = psycopg2.connect(config.database_url)
cursor = conn.cursor()

# Get users table structure
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'users'
    ORDER BY ordinal_position;
""")

print("Users table structure:")
for col_name, data_type, is_nullable in cursor.fetchall():
    nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
    print(f"  {col_name}: {data_type} {nullable}")

conn.close()

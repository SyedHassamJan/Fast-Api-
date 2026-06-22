import psycopg2
from app.config.app_config import getAppConfig

config = getAppConfig()
conn = psycopg2.connect(config.database_url)
cursor = conn.cursor()

try:
    # Add name column if it doesn't exist
    cursor.execute("""
        ALTER TABLE users
        ADD COLUMN name VARCHAR(191) NOT NULL DEFAULT '';
    """)
    conn.commit()
    print("✓ Name column added successfully")
except psycopg2.errors.DuplicateColumn:
    print("Column 'name' already exists")
    conn.rollback()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

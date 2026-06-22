import psycopg2
from app.config.app_config import getAppConfig

config = getAppConfig()
# Parse the connection string
conn = psycopg2.connect(config.database_url)
cursor = conn.cursor()

# Clear the alembic_version table
cursor.execute("DELETE FROM alembic_version;")
conn.commit()

print("Migration history cleared from database")

cursor.close()
conn.close()

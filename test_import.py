#!/usr/bin/env python
import sys
print("Python version:", sys.version)
print("Python path:", sys.executable)

# Try importing step by step
print("\n1. Importing datetime...")
from datetime import datetime, timezone
print("   Success")

print("\n2. Importing sqlalchemy...")
from sqlalchemy import Boolean, Column, DateTime, Integer, String, VARCHAR
print("   Success")

print("\n3. Importing app.database.db...")
from app.database.db import Base
print("   Success")

print("\n4. Creating TodoSchema class...")
class TodoSchema(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.now(timezone.utc))

print("   Success - TodoSchema:", TodoSchema)

print("\n5. Checking what's in the module file...")
import app.database.schema.todo_schema as todo_mod
print("   Module contents:", [x for x in dir(todo_mod) if not x.startswith('_')])

print("\n6. Trying to get TodoSchema attribute...")
try:
    cls = getattr(todo_mod, 'TodoSchema')
    print("   Success:", cls)
except AttributeError as e:
    print("   Error:", e)

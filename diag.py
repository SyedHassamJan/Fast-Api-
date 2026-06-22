import app.database.schema as schema_pkg
print("schema package file:", schema_pkg.__file__)
print("schema package contents:", dir(schema_pkg))

from app.database.db import Base
print("Before import - tables:", list(Base.metadata.tables.keys()))

from app.database.schema import TodoSchema
print("After import - tables:", list(Base.metadata.tables.keys()))
print("TodoSchema class:", TodoSchema)
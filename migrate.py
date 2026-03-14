# migrate_add_rating_remarks.py  — run once from the project root
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from peewee import FloatField, TextField
from playhouse.migrate import SqliteMigrator, migrate

from rose.database import db

db.connect(reuse_if_open=True)
migrator = SqliteMigrator(db)

migrate(
    migrator.add_column("book", "user_rating", FloatField(default=0)),
    migrator.add_column("book", "user_remarks", TextField(null=True)),
)

db.close()
print("Migration complete.")

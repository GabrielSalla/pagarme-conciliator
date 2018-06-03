from importlib import util
import src.prod_database as prod_database_controller
import src.models as models
import peewee
import re
import os
import sys


def restart_database():
    print("Erasing the database")
    statements = (
        "drop schema if exists public cascade;"
        "create schema public;"
        "create extension hstore;"
    )
    prod_database_controller.database.execute_sql(statements)


def apply_migrations(clear=False):
    if clear:
        restart_database()

    # Load the migrations from the migrations folder
    path = os.path.join(".", "migrations")
    migrations = sorted(filter(
        lambda file_name: re.match(r"\d{8}_\d{2}.py", file_name) is not None,
        os.listdir(path)
    ))

    # Get the last migration applied
    try:
        last_migration = models.Migration.select().order_by(
            models.Migration.id.desc()).get()
    except peewee.ProgrammingError:
        last_migration = None

    # Filter to apply only the new migrations
    if last_migration is not None:
        migrations = list(filter(
            lambda migration: migration > last_migration.name, migrations))

    print("Applying migrations")
    for migration in migrations:
        print("  ", migration)
        migration_path = os.path.join(".", "migrations", migration)
        spec = util.spec_from_file_location(migration, migration_path)
        migration_import = util.module_from_spec(spec)
        spec.loader.exec_module(migration_import)
        migration_import.apply()
        applyied_migration = models.Migration(name=migration)
        applyied_migration.save()

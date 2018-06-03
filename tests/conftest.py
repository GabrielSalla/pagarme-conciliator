import src.prod_database as prod_database_controller
import scripts.migrations as migrations_utils
from _pytest.monkeypatch import MonkeyPatch
import asyncio
import pytest


# Generate a session event_loop fixture
@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


# Generate a session monkeypatch fixture
@pytest.fixture(scope="session")
def monkeypatch_session():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


# Automatically setup the production database and the production database
# controller
@pytest.fixture(scope="session", autouse=True)
async def setup_prod_database_controller():
    # Clear database and apply migrations in the correct order
    migrations_utils.apply_migrations(True)
    yield
    prod_database_controller.close_connections()

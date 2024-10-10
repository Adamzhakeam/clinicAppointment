'''
    this module is responsible for handling migrations 
'''
from __future__ import with_statement
import sys
import os

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Import your application and database instance
from models import db  # Import your db instance
from app import app  # Import your Flask app

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = db.Model.metadata  # This gets the metadata from your models

# Other setup can go here if needed
def get_engine():
    return engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# This is the entry point of the script
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from logging.config import fileConfig
from app.core.config import settings

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.database import Base  # Import your SQLAlchemy Base
from app.models import *  # Optional: force model import for autogeneration


# Get Alembic config
config = context.config

# ✅ Safely get DATABASE_URL
database_url =settings.DATABASE_URL
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set or is empty.")

# Set sqlalchemy.url for Alembic
config.set_main_option("sqlalchemy.url", database_url)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""env.py

Database configuration and migration helper functions.
"""

from alembic import context
from flask import current_app
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

config = context.config
fileConfig(config.config_file_name)

config.set_main_option(
    'sqlalchemy.url',
    current_app.config.get('SQLALCHEMY_DATABASE_URI')
)

target_metadata = current_app.extensions['migrate'].db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an
    Engine is acceptable here as well.  By skipping the Engine creation we
    don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context.
    """
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

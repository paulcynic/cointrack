#! /usr/bin/env bash


# To create all tables and columns for the first time
alembic revision --autogenerate -m "First migration"

# Run migrations for the first time
alembic upgrade head
# When you make any change to a database table,
# you capture that change by running
## alembic revision --autogenerate -m "Some description"

# Let the DB start
python ./backend_pre_start.py
# Create initial data in DB
python ./initial_data.py


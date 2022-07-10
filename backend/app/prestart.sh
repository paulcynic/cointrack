#! /usr/bin/env bash

# Let the DB start
python ./backend_pre_start.py

# Run migrations for the first time
alembic upgrade head
# When you make any change to a database table,
# you capture that change by running
## alembic revision --autogenerate -m "Some description"

# Create initial data in DB
python ./initial_data.py

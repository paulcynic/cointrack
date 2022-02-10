# Cointrack
***Cointrack is an app for tracking cryptocurrency with telegram-bot notification.***

![coin tracker image](../master/docs/_static/ex_show_price.png)

- [Installation](#installation)
- [Setup instruction](#setup-instruction)
- [Remarks](#remarks)

## How to use

1. Choose a coin from the list.
2. Choose a currency from the list.
3. Push "show current price" 
   - or push "show all coins" to see the price for all coins.
4. Enter lower and upper limits.
5. Push "follow coin".
6. If the price of the selected coin changes, the telegram bot will notify you. 

## Installation

From your linux terminal:
`git clone https://github.com/paulcynic/cointrack.git`

## Setup instruction

1. First you need to install [Poetry](https://python-poetry.org/) in your working directory.
    `pip install poetry`
2. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
3. Enter into your database \(example of using postgres\):
    ```
    # Linux
    psql -h localhost -U username -d your_db

    your_db=# CREATE DATABASE 'your_db';
    ```
4. Check and update your database config in 
    `cointrack/app/core/config.py`
    >`SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pg_username:pg_password@localhost:5432/your_db`
5. Remove all files from the directory `cointrack/alembic/versions/`
    `rm cointrack/alembic/versions/*.py`
6. Run the Database via poetry `poetry run ./prestart.sh`
7. Check manually your database if all tables were created.
8. Run the FastAPI server via poetry. [^note]
    `poetry run ./run.sh`
10. Open http://localhost:8002/
 
## Remarks
Write in `cointrack/run.sh` your personal variables.
```
#!/bin/sh
export SECRET_KEY='your_secret_key'
export DB_PASS='your_db_password'
export SOME_YOURS_VARIABLES='something'
export API_TOKEN='your_api_token'
...
export APP_MODULE=${APP_MODULE-app.main:app}

export HOST=${HOST:-0.0.0.0}

export PORT=${PORT:-8002}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"
```

@paulcynic :+1:

[^note]: Personalize defaults through environment variables [here](#remarks)


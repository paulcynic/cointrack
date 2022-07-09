FROM python:3.10
WORKDIR /app/

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application (e.g. django logs)
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

COPY ./app /app

# Install dependecies
RUN pip3 install -r /app/requirements.txt --no-cache-dir && \
    pip3 uninstall pip -y

ENV PYTHONPATH=/app
# And then will start Uvicorn
CMD ["./run.sh"]

FROM ubuntu:22.10 AS base-image

RUN apt-get update && apt-get install --no-install-recommends -y \
    gunicorn \
    curl \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base-image

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY migrations /app/migrations
COPY ./app /app/app
COPY VERSION ./app/VERSION
COPY ./helpers /app/helpers
COPY ./games.py /app/games.py

ENV FLASK_APP=games.py
# /dev/shm removes the deadlock waiting for a file to write to
# --accesslog-file=-   ---> write to standard out
# --log-file=-   ---> write errors to standard err
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=2 --threads=2 --worker-tmp-dir /dev/shm --access-logfile=- --log-file=-"

CMD ["gunicorn", "games:APP"]

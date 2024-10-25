FROM python:3.11-slim-bullseye

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./bot /src/bot

CMD ["bash", "-c", "python -m bot.database.session && python -m bot"]
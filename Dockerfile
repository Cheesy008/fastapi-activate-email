FROM python:3.7-slim-buster

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

CMD ["/code/entrypoint.sh"]

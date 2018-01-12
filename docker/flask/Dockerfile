FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN groupadd -r flask && useradd -r -g flask flask

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app/src
RUN cd /app/src && python setup.py bdist_wheel && pip install ./dist/*.whl 

ENV FLASK_APP=/app/src/docker/flask/helloworld.py

CMD ["flask", "run"]

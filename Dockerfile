FROM python:3.9-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Setup
RUN pip install pipenv

# Copy local code to the container image.
WORKDIR /app
COPY Pipfile.lock /app
RUN pipenv sync --system
COPY . /app

EXPOSE 8080

ENV FLASK_APP=src/api/app.py

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
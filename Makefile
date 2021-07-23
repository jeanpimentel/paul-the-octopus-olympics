.PHONY: run deps format clean build deploy

GCP_PROJECT=project-id
LOGIN=login

all: deps

run:
	FLASK_APP=src/api/app.py pipenv run flask run --host=0.0.0.0 --port=8080

deps:
	@echo "Installing dependencies..."
	@pipenv sync --dev --pre

format:
	@pipenv run black src

clean:
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

build: clean
	@echo "Building the container for project ${GCP_PROJECT} and login ${LOGIN}"
	docker build -t gcr.io/${GCP_PROJECT}/${LOGIN}-player .
	docker push gcr.io/${GCP_PROJECT}/${LOGIN}-player

deploy: build
	@echo "Deploying Cloud Run for project ${GCP_PROJECT} and login ${LOGIN}"
	gcloud run deploy ${LOGIN}-player --image gcr.io/${GCP_PROJECT}/${LOGIN}-player --platform managed --region us-west1 --allow-unauthenticated
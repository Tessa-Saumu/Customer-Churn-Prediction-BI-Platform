IMAGE_NAME := customer-churn-api
CONTAINER_NAME := customer-churn-api
PORT := 8000

.PHONY: help build run start stop restart logs test shell clean rebuild train \
        health api

help:
	@echo "Customer Churn Prediction & BI Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  make build    Build Docker image and train model"
	@echo "  make run      Run container in foreground"
	@echo "  make start    Build image and start container"
	@echo "  make stop     Stop container"
	@echo "  make restart  Restart container"
	@echo "  make logs     Follow container logs"
	@echo "  make test     Run pytest"
	@echo "  make health   Check API health"
	@echo "  make api      Open API documentation URL"
	@echo "  make shell    Open shell inside container"
	@echo "  make clean    Remove container"
	@echo "  make rebuild  Clean and rebuild image"
	@echo ""

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		-p $(PORT):8000 \
		$(IMAGE_NAME)

start: build
	docker run -d \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		-p $(PORT):8000 \
		$(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) 2>/dev/null || true

restart: stop start

logs:
	docker logs -f $(CONTAINER_NAME)

test:
	python -m pytest

health:
	curl http://localhost:$(PORT)/health

api:
	@echo "API: http://localhost:$(PORT)"
	@echo "Swagger: http://localhost:$(PORT)/docs"
	@echo "ReDoc: http://localhost:$(PORT)/redoc"

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

clean:
	docker stop $(CONTAINER_NAME) 2>/dev/null || true
	docker rm $(CONTAINER_NAME) 2>/dev/null || true

rebuild: clean
	docker build --no-cache -t $(IMAGE_NAME) .
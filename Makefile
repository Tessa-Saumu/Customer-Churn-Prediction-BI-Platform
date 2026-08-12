IMAGE_NAME := customer-churn-api
CONTAINER_NAME := customer-churn-api
API_PORT := 8000
STREAMLIT_PORT := 8501

.PHONY: help build run start stop restart logs logs-api logs-ui \
        test test-api status shell clean rebuild

help:
	@echo ""
	@echo "Customer Churn Prediction & BI Platform"
	@echo ""
	@echo "Docker commands:"
	@echo "  make build       Build API and Streamlit images"
	@echo "  make run         Start services in foreground"
	@echo "  make start       Start services in background"
	@echo "  make stop        Stop services"
	@echo "  make restart     Restart services"
	@echo "  make logs        Follow all logs"
	@echo "  make logs-api    Follow API logs"
	@echo "  make logs-ui     Follow Streamlit logs"
	@echo "  make status      Show service status"
	@echo "  make shell       Open API container shell"
	@echo "  make clean       Stop and remove containers"
	@echo "  make rebuild     Rebuild images without cache"
	@echo ""
	@echo "Testing:"
	@echo "  make test        Run pytest"
	@echo "  make test-api    Test API health endpoint"
	@echo ""

build:
	docker compose build

run:
	docker compose up

start:
	docker compose up -d

stop:
	docker compose down

restart:
	docker compose down
	docker compose up -d

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

logs-ui:
	docker compose logs -f streamlit

status:
	docker compose ps

test:
	python -m pytest

test-api:
	curl --fail http://localhost:$(API_PORT)/health
	@echo ""
	@echo "API health check passed."

shell:
	docker compose exec api /bin/bash

clean:
	docker compose down --remove-orphans

rebuild:
	docker compose down --remove-orphans
	docker compose build --no-cache
	docker compose up -d
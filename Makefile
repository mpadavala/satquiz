.PHONY: help setup-backend setup-frontend dev-backend dev-frontend dev docker-up docker-down migrate test

help:
	@echo "Available commands:"
	@echo "  make setup-backend    - Set up backend environment"
	@echo "  make setup-frontend   - Set up frontend environment"
	@echo "  make dev-backend      - Run backend in development mode"
	@echo "  make dev-frontend     - Run frontend in development mode"
	@echo "  make dev              - Run both backend and frontend"
	@echo "  make docker-up        - Start all services with Docker Compose"
	@echo "  make docker-down      - Stop all services"
	@echo "  make migrate          - Run database migrations"
	@echo "  make test             - Run tests"

setup-backend:
	cd backend && python -m venv venv && \
	. venv/bin/activate && pip install -r requirements.txt

setup-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev

dev: dev-backend dev-frontend

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	cd backend && . venv/bin/activate && alembic upgrade head

test:
	cd backend && . venv/bin/activate && pytest
	cd frontend && npm test

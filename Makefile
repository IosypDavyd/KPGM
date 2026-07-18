# Makefile for KPGM

.PHONY: help install dev test clean docker up down

help:
	@echo "KPGM Music Video Generator"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make dev         Start development servers"
	@echo "  make test        Run tests"
	@echo "  make clean       Clean up files"
	@echo "  make docker      Start with Docker"
	@echo "  make up          Start Docker services"
	@echo "  make down        Stop Docker services"

install:
	@echo "📦 Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd ../frontend && npm install
	@echo "✓ Installation complete"

dev:
	@echo "🚀 Starting development servers..."
	@bash start-dev.sh

test:
	@echo "🧪 Running tests..."
	cd backend && pytest tests/ -v

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.pytest_cache
	rm -rf frontend/node_modules
	rm -rf frontend/build
	rm -f *.db
	@echo "✓ Cleanup complete"

docker:
	@echo "🐳 Starting with Docker..."
	@bash start-docker.sh

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

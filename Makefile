.PHONY: help install migrate run test clean

help:
	@echo "Medical MAS - Makefile Commands"
	@echo "================================"
	@echo "install       - Install dependencies"
	@echo "migrate       - Run database migrations"
	@echo "run           - Run development server"
	@echo "celery        - Run Celery worker"
	@echo "test          - Run tests"
	@echo "lint          - Run code quality checks"
	@echo "format        - Format code with black and isort"
	@echo "clean         - Clean temporary files"
	@echo "superuser     - Create superuser"
	@echo "shell         - Open Django shell"

install:
	pip install -r requirements/dev.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

celery:
	celery -A config worker -l info

celery-beat:
	celery -A config beat -l info

test:
	pytest

test-cov:
	pytest --cov=apps --cov-report=html --cov-report=term

lint:
	flake8 apps config
	pylint apps config
	mypy apps config

format:
	black apps config tests
	isort apps config tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell_plus

loaddata:
	python manage.py loaddata fixtures/diseases.json

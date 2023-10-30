.PHONY: all
run:
	poetry run python src/main.py 
build:
	docker-compose up --build
delete:
	docker system prune -a -f --filter "until=24h"
	docker system prune --volumes -f

lint:
	poetry run ruff .
	poetry run pflake8 src
	poetry run isort --check --diff .
	poetry run black --check .
	poetry run mypy .

format:
	poetry run isort .
	poetry run black .
	poetry run ruff --fix .


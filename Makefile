migrate:
	docker-compose exec backend alembic -c ./app/alembic.ini upgrade head

lint:
	flake8 ./app

format:
	black .

isort:
	isort .

test-cov:
	pytest tests/ --cov=app --cov-report=term-missing

.PHONY: bootstrap run test lint docker terraform

bootstrap:
	./scripts/bootstrap.sh

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

test:
	pytest -v

lint:
	ruff check .

docker:
	docker build -t system-health-check-api .

terraform:
	cd terraform && terraform init && terraform validate
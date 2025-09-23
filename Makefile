.DEFAULT_GOAL := help

run:
	poetry run uvicorn main:app --host localhost --port 8000 --reload --env-file .local.env


install:
	@echo "Installing dependency: $(filter-out $@,$(MAKECMDGOALS))"
	poetry add $(filter-out $@,$(MAKECMDGOALS))


uninstall:
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

help:
	@echo "Usage make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-Za-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ".*?## "}; {printf " %-20s %s\n", $$1, $$2}'

update:
	@echo "Updating Poetry to the latest version..."
	poetry self update
	@echo "Updating all dependencies..."
	poetry update

migrate-apply:
	poetry run alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

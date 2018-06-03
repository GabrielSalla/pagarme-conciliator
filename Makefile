OPERATION=all

init:
	@touch .session_id

build-prod:
	@docker-compose build pagarme-conciliator-prod

build-test:
	@docker-compose build pagarme-conciliator-prod
	@docker-compose build pagarme-conciliator-test

up-database:
	@docker-compose up -d postgres-prod

down-database:
	@docker-compose stop postgres-test
	@docker-compose stop postgres-prod

migrate:
	@docker-compose run --rm pagarme-conciliator-prod-local python3 -c 'from scripts.migrations import apply_migrations; apply_migrations()'

restart-database:
	@docker-compose run --rm pagarme-conciliator-prod-local python3 -c 'from scripts.migrations import apply_migrations; apply_migrations(True)'

conciliate:
	@docker-compose run --rm pagarme-conciliator-prod-local python3 . $(OPERATION)

test-docker:
	@docker-compose run --rm pagarme-conciliator-test

test-tox:
	@tox

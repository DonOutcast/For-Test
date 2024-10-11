.DEFAULT_GOAL := help
.PHONY: help run up stop logs migrations migrate show_migrations migrations_docker migrate_docker show_migrations_docker create_super_user_docker

SHELL := /bin/bash
LOCAL_COMPOSE_FILE := docker-compose.yml

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_WHITE = \033[00m

help:  # show help
	@echo -e "$(COLOR_GREEN)Makefile help:"
	@grep -E "^[a-zA-Z0-9_-]+:.*#"  Makefile | sort | while read -r l; do printf "$(COLOR_GREEN)  $$(echo $$l | cut -f 1 -d':'):$(COLOR_WHITE)$$(echo $$l | cut -f 2- -d'#')\n"; done

run: env up migrations_docker migrate_docker create_super_user_docker# Run all

env: # Make .env file
	@echo -e "$(COLOR_YELLOW)Rename .env-example to .env$(COLOR_RESET)"
	@cp .env-example .env
	@echo -e "$(COLOR_GREEN)The .env file is ready$(COLOR_RESET)"

up: # up all docker services
	@echo -e "$(COLOR_YELLOW)Run services...$(COLOR_RESET)"
	@docker-compose --profile all up --build -d
	@echo -e "$(COLOR_GREEN)Services are running$(COLOR_RESET)"

stop: # stop all services
	@echo -e "$(COLOR_YELLOW)Stop services...$(COLOR_RESET)"
	@docker-compose --profile all stop
	@echo -e "$(COLOR_GREEN)Services stopped$(COLOR_RESET)"

logs: # get last logs
	@echo -e "$(COLOR_YELLOW)Last logs:$(COLOR_RESET)"
	@docker-compose -f $(LOCAL_COMPOSE_FILE) --profile all logs --tail=100 -f $(c)

migrations_docker: # generate migration in docker container
	@echo -e "$(COLOR_GREEN)Rum Django makemigrations$(COLOR_RESET)"
	@docker exec -it django_service python3 manage.py makemigrations
	@echo -e "$(COLOR_GREEN)Migrations are make$(COLOR_RESET)"

migrate_docker: # run migrations in docker container
	@echo -e "$(COLOR_GREEN)Rum Django migrate$(COLOR_RESET)"
	@docker exec -it django_service python3 manage.py migrate
	@echo -e "$(COLOR_GREEN)Migrations are migrated$(COLOR_RESET)"

show_migrations_docker: # show history of migrations in docker container
	@echo -e "$(COLOR_GREEN)Rum Django showmigrations$(COLOR_RESET)"
	@docker exec -it django_service python3 manage.py showmigrations
	@echo -e "$(COLOR_GREEN)Migrations shown(COLOR_RESET)"

create_super_user_docker: # create a custom super user
	@echo -e "$(COLOR_GREEN)Rum Django create_supser_user$(COLOR_RESET)"
	@docker exec -it django_service python3 manage.py create_super_user
	@echo -e "$(COLOR_GREEN)The super user are created(COLOR_RESET)"

migrations: # generate migration
	@echo -e "$(COLOR_GREEN)Rum Django makemigrations$(COLOR_RESET)"
	@python3 backed/manage.py makemigrations
	@echo -e "$(COLOR_GREEN)Migrations are make$(COLOR_RESET)"

migrate: # run migrations
	@echo -e "$(COLOR_GREEN)Rum Django migrate$(COLOR_RESET)"
	@python3 backed/manage.py migrate
	@echo -e "$(COLOR_GREEN)Migrations are migrated$(COLOR_RESET)"

show_migrations:#show history of migrations
	@echo -e "$(COLOR_GREEN)Rum Django showmigrations$(COLOR_RESET)"
	@python3 backed/manage.py showmigrations
	@echo -e "$(COLOR_GREEN)Migrations shown(COLOR_RESET)"

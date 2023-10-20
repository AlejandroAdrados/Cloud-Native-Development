# If you want you can use this Makefile to specify debug commands, test scripts, etc.

# Some examples below

start-backend:
	docker-compose -f g7t2/docker-compose.yml up -d

start-all:
	docker-compose up -d

restart:
	docker-compose restart

build:
	docker-compose build

purge:
	docker-compose down -v --rmi all --remove-orphans

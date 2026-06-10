#!make

GIT_HASH := $(shell git rev-parse --short HEAD)

assignment-2:	cleanup build run test

cleanup: 
	docker compose down --remove-orphans

build:
	cd ./17636-service-first/ && \
		docker build -t soobinrho/17636-service-first:latest \
		-t soobinrho/17636-service-first:$(GIT_HASH) .
	cd ./17636-service-second/ && \
		docker build -t soobinrho/17636-service-second:latest \
		-t soobinrho/17636-service-second:$(GIT_HASH) .

run:
	docker compose up --detach
	sleep 5

test:
	curl http://127.0.0.1/romeo-and-juliet/thy --silent | jq
	curl http://127.0.0.1/romeo-and-juliet/love --silent | jq
	curl http://127.0.0.1/romeo-and-juliet/delicious --silent | jq
	curl http://127.0.0.1/romeo-and-juliet/food --silent | jq
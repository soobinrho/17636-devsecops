#!make

GIT_HASH := $(shell git rev-parse --short HEAD)

assignment-2:	build run test

build:
	cd ./17636-service-first/ && \
		docker build -t soobinrho/17636-service-first:latest \
		-t soobinrho/17636-service-first:$(GIT_HASH) .
	cd ./17636-service-second/ && \
		docker build -t soobinrho/17636-service-second:latest \
		-t soobinrho/17636-service-second:$(GIT_HASH) .


run:
# 	docker compose


test:
	curl http://127.0.0.1/romeo-and-juliet/thy
	curl http://127.0.0.1/romeo-and-juliet/love
	curl http://127.0.0.1/romeo-and-juliet/delicious
	curl http://127.0.0.1/romeo-and-juliet/food
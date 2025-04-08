DATA_DIR ?= data
IMAGE_NAME ?= fancy-todo
IMAGE_TAG ?= latest

build:
	docker build -t todo-flask-app .

run:
	poetry run python main.py

run-local-docker: clean build
	docker run -p 5001:5001 \
		-e DATA_DIR=$(DATA_DIR) \
		-v $$(pwd)/$(DATA_DIR):/app/data \
		--name todo-flask-app \
		todo-flask-app

run-real-docker:
	docker run -p 5001:5001 \
		-e DATA_DIR=$(DATA_DIR) \
		-v $$(pwd)/$(DATA_DIR):/app/data \
		--name todo-flask-app \
		nfarmer371/fancy-todo:latest

clean:
	docker stop todo-flask-app
	docker rm todo-flask-app

# login: docker login
# configure image version: make push IMAGE_NAME=fancy-todo IMAGE_TAG=v1.0.0
push:
	docker build -t nfarmer371/$(IMAGE_NAME):$(IMAGE_TAG) .
	docker push nfarmer371/$(IMAGE_NAME):$(IMAGE_TAG)
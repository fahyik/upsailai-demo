# Variables
PROJECT_ID := upsailai-demo
IMAGE_NAME := discord-bot
TAG := v0
GCR_IMAGE := gcr.io/$(PROJECT_ID)/$(IMAGE_NAME):$(TAG)
PERSIST_DIR := $(PWD)/data/chroma_db
DOCSTORE_PATH := $(PWD)/data/doc_store

# Docker commands
DOCKER := docker
DOCKER_BUILD := $(DOCKER) build
DOCKER_RUN := $(DOCKER) run
DOCKER_PUSH := $(DOCKER) push

# GCP command
GCLOUD := gcloud
GCLOUD_AUTH := $(GCLOUD) auth configure-docker

.PHONY: all build push test gcp-login

# Default action to build, push, and test
all: build push test

# Build the Docker image
build:
	$(DOCKER_BUILD) -t $(GCR_IMAGE) .

# Push the Docker image to GCR
push:
	$(DOCKER_PUSH) $(GCR_IMAGE)

# Authenticate with GCR
gcp-login:
	$(GCLOUD_AUTH)

# Run the Docker container locally for testing
test:
	$(DOCKER_RUN) --rm -it \
		-v $(PWD)/.env:/app/.env \
		-e PERSIST_DIR=/app/persisted_vector_store \
		-e DOCSTORE_PATH=/app/docstore \
		-v $(PERSIST_DIR):/app/persisted_vector_store \
		-v $(DOCSTORE_PATH):/app/docstore \
		$(GCR_IMAGE)

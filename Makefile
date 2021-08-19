VERSION="v0.0.1"

version:
	@echo ${VERSION}

IMAGE_TAG ?= $(shell git describe --tags)

.PHONY: images
images:
	docker build -t hulyndon/pyboot:${IMAGE_TAG} -f _build/Dockerfile .


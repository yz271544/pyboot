VERSION="v3.0.0"
# usage:
# base images: make images IMAGE_TAG=latest REPO=docker.gridsumdissector.com/
# tensorflow images: make image-on-tensorflow IMAGE_TAG=latest REPO=docker.gridsumdissector.com/
version:
	@echo ${VERSION}

# config you want to tag
IMAGE_TAG ?= $(shell git describe --tags)
# config your docker repository address
REPO ?= docker.gridsumdissector.com/

.PHONY: images
images:
	docker build -t ${REPO}kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile .

.PHONY: image-on-tensorflow
image-on-tensorflow:
	docker build -t ${REPO}kubeedge/pyboot-tensorflow:${IMAGE_TAG} -f _build/tensorflow.Dockerfile .

.PHONY: cross-build
cross-build: cross-build-amd64 cross-build-arm64

.PHONY: cross-build-amd64
cross-build-amd64:
	docker buildx build --platform linux/amd64 -t ${REPO}kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile . --push

.PHONY: cross-build-arm64
cross-build-arm64:
	docker buildx build --platform linux/arm64 -t ${REPO}kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile-arm64 . --push

# Copyright 2021 The KubeEdge Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
.EXPORT_ALL_VARIABLES:
# config you want to tag
IMAGE_TAG ?= $(shell git describe --tags)
PLATFORMS ?= linux/amd64,linux/arm64
# config your docker repository address
IMAGE_REPO ?= docker.gridsumdissector.com

.PHONY: images
images: images-amd64 images-arm64

.PHONY: images-amd64
images-amd64:
	docker build -t ${IMAGE_REPO}/kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile-amd64.docker .

.PHONY: images-arm64
images-arm64:
	docker build -t ${IMAGE_REPO}/kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile-arm64.docker .


.PHONY: image-on-tensorflow
image-on-tensorflow:
	docker build -t ${IMAGE_REPO}/kubeedge/pyboot-tensorflow:${IMAGE_TAG} -f _build/tensorflow.Dockerfile .

.PHONY: cross-build
ifeq ($(HELP),y)
cross-build:
	@echo "docker cross build in platform ${PLATFORMS}"
else
cross-build:
	echo "PLATFORMS:${PLATFORMS}"
	_build/cross-build.sh ${PLATFORMS}
endif
# cross-build: cross-build-amd64 cross-build-arm64

.PHONY: cross-build-amd64
cross-build-amd64:
	docker buildx build --platform linux/amd64 -t ${IMAGE_REPO}/kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile-amd64.docker . --push

.PHONY: cross-build-arm64
cross-build-arm64:
	docker buildx build --platform linux/arm64 -t ${IMAGE_REPO}/kubeedge/pyboot:${IMAGE_TAG} -f _build/Dockerfile-arm64.docker . --push

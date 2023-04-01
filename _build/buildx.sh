#!/usr/bin/env bash

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

# update the code from https://github.com/kubeedge/sedna/blob/e95caf947141bf9b2a4b92aa19c8ad9d5ce677ae/hack/lib/buildx.sh

set -o errexit
set -o nounset
set -o pipefail

pyboot::buildx::prepare_env() {
  # Check whether buildx exists.
  if ! docker buildx >/dev/null 2>&1; then
    echo "ERROR: docker buildx not available. Docker 19.03 or higher is required with experimental features enabled" >&2
    exit 1
  fi

  # Use tonistiigi/binfmt that is to enable an execution of different multi-architecture containers
  docker run --privileged --rm tonistiigi/binfmt --install all

  # Create a new builder which gives access to the new multi-architecture features.
  builder_instance="pyboot-buildx"
  if ! docker buildx inspect $builder_instance >/dev/null 2>&1; then
    docker buildx create --use --name $builder_instance --driver docker-container
  fi
  docker buildx use $builder_instance
}

pyboot::buildx:generate-dockerfile() {
  dockerfile=${1}
  sed "s/FROM/FROM --platform=\$BUILDPLATFORM/g" ${dockerfile}
}

pyboot::buildx::push-multi-platform-images() {
  pyboot::buildx::prepare_env

  echo "pushing ${PLATFORMS} image for $component"

  temp_dockerfile=_build/buildx_dockerfile
  pyboot::buildx:generate-dockerfile _build/Dockerfile > ${temp_dockerfile}

  docker buildx build --push \
    --build-arg GO_LDFLAGS="${GO_LDFLAGS}" \
    --platform ${PLATFORMS} \
    -t ${IMAGE_REPO}/pyboot:${IMAGE_TAG} \
    -f ${temp_dockerfile} .

  rm ${temp_dockerfile}
}

pyboot::buildx::build-multi-platform-images() {
#  pyboot::buildx::prepare_env
  echo "INPUT: $1"
  PLATFORMS=$1
  echo "PLATFORMS:$PLATFORMS"
  arch_array=(${PLATFORMS//,/ })

  for arch in ${arch_array[@]}; do
    echo "arch:${arch} ddd: ${arch##*/}"
    temp_dockerfile=${PYBOOT_OUTPUT_IMAGEPATH}/buildx_dockerfile_${arch##*/}
    pyboot::buildx:generate-dockerfile _build/Dockerfile-${arch##*/}.docker > ${temp_dockerfile}
    tag_name=${IMAGE_REPO}/pyboot:${IMAGE_TAG}-${arch##*/}
    echo "building ${arch} image tag name is ${tag_name}"

    docker buildx build -o type=docker \
      --platform ${arch} \
      -t ${tag_name} \
      -f ${temp_dockerfile} .

    rm ${temp_dockerfile}
  done


}

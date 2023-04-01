#!/usr/bin/env bash

# Copyright 2020 The KubeEdge Authors.
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

# copy from https://github.com/kubeedge/kubeedge/blob/081d4f245725d44f23d9a2919db99a01c56a83e9/hack/lib/init.sh

set -o errexit
set -o nounset
set -o pipefail

# The root of the edgemesh
PYBOOT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

PYBOOT_OUTPUT_SUBPATH="${PYBOOT_OUTPUT_SUBPATH:-_output/local}"
PYBOOT_OUTPUT="${PYBOOT_ROOT}/${PYBOOT_OUTPUT_SUBPATH}"
PYBOOT_OUTPUT_BINPATH="${PYBOOT_OUTPUT}/bin"
PYBOOT_OUTPUT_IMAGEPATH="${PYBOOT_OUTPUT}/image"
mkdir -p ${PYBOOT_OUTPUT_IMAGEPATH}

source "${PYBOOT_ROOT}/_build/buildx.sh"

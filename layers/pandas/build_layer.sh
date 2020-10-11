#!/usr/bin/env bash

export package_dir="python"

rm -rf "${package_dir}" && mkdir -p "${package_dir}"

docker run --rm -v $(pwd):/foo -w /foo --user 1000:1000 lambci/lambda:build-python3.8 \
    pip install -r layer_requirements.txt --no-deps -t "${package_dir}" 2> /dev/null
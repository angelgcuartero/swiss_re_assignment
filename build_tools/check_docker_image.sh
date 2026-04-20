#!/bin/bash

package_name=$(grep 'name' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')
version=$(grep 'version' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')

docker run -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL,HIGH,UNKNOWN "${package_name}":"${version}"

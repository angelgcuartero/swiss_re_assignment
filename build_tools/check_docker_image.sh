#!/bin/bash

package_name=$(grep 'name' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')
version=$(grep 'version' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')

if docker run -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity CRITICAL,HIGH,UNKNOWN "${package_name}":"${version}"; then
   echo -e "\nDocker image '${package_name}:${version}' checked successfully and no critical, high, or unknown vulnerabilities were found"
else
   echo -e "\nCheck failed so the Docker image may have vulnerabilities that need to be addressed"
fi

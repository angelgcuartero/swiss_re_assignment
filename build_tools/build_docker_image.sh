#!/bin/bash

package_name=$(grep 'name' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')
version=$(grep 'version' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')

echo -e "\nBuilding the Docker image $package_name:$version"
docker build --tag "${package_name}":"${version}" .
if [ $? -eq 0 ]; then
   echo -e "\nDocker image created successfully and tagged as '${package_name}:${version}'"
else
   echo -e "\nBuild failed so the Docker image was not be created"
fi
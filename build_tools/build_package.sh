#!/bin/bash

package_name=$(grep 'name' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')
version=$(grep 'version' pyproject.toml | awk -F '=' '{print $2}' |  tr -d '", ')

if uv build --no-cache; then
   echo -e "\nPackage built successfully and versioned as '${package_name}:${version}'"
else
   echo -e "\nBuild failed so the package was not be created"
fi

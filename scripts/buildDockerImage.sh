#!/bin/bash

# Directory of buildDockerImage.sh script :
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Buildling the Docker image for wolfdotsolar :
docker build -t wolfdotsolar "$DIR/../Docker/"
#!/bin/bash

# Directory of buildDockerImage.sh script :
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Going to the project root directory :
cd "$DIR/.."

# Buildling the Docker image for wolfdotsolar :
docker build -t wolfdotsolar -f Docker/Dockerfile .
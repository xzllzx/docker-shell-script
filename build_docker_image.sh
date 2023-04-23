#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Declare a dictionary of version numbers and their corresponding git SHAs
declare -A version_and_sha=(
    ["1.0.0"]="GIT_SHA_1"
    ["1.1.0"]="GIT_SHA_2"
    # Add more versions and SHAs here
)

# Iterate through the dictionary and build, tag, and push the Docker images
for version in "${!version_and_sha[@]}"; do
    sha=${version_and_sha[$version]}

    # Clone the specific version of the repository
    git clone https://github.com/your_username/your_repository.git --branch $sha ./temp_repo

    # Build the Docker image with the specific version number
    docker build -t source:$version ./temp_repo

    # Tag the Docker image with your Docker Hub username and repository
    docker tag source:$version $DOCKER_USERNAME/source:$version

    # Push the Docker image to Docker Hub
    docker push $DOCKER_USERNAME/source:$version

    # Clean up the temporary repository folder
    rm -rf ./temp_repo
done

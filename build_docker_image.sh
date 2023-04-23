#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Declare a dictionary of version numbers and their corresponding git SHAs
declare -A version_and_sha=(
    ["1.0"]="bfeb478a55240c332a8e6b28e689d549e10ddbec",
    ["2.0"]="8153df2c37bcea4a4beeb090851903150d7f1633",
    ["3.0"]="da634bf2c1e6bbfb36cc3172966ede6c9a8c7dc8",
)

# Iterate through the dictionary and build, tag, and push the Docker images
for version in "${!version_and_sha[@]}"; do
    sha=${version_and_sha[$version]}

    # Clone the specific version of the repository using the personal access token
    git clone https://${GIT_ACCESS_TOKEN}@{GIT_REPOSITORY} --branch $sha ./temp_repo

    # Build the Docker image with the specific version number
    docker build -t {IMAGE_NAME}:$version ./temp_repo

    # Tag the Docker image with your Docker Hub username and repository
    docker tag {IMAGE_NAME}:$version ${DOCKER_USERNAME}/{IMAGE_NAME}:$version

    # Push the Docker image to Docker Hub
    docker push ${DOCKER_USERNAME}/{IMAGE_NAME}:$version

    # Clean up the temporary repository folder
    rm -rf ./temp_repo
done

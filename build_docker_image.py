import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Declare a dictionary of version numbers and their corresponding git SHAs
version_and_sha = {
    "1.0.0": "GIT_SHA_1",
    "1.1.0": "GIT_SHA_2",
    # Add more versions and SHAs here
}

DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")

for version, sha in version_and_sha.items():
    # Clone the specific version of the repository
    subprocess.run(["git", "clone", "https://github.com/your_username/your_repository.git", "--branch", sha, "./temp_repo"])
    
    # Build the Docker image with the specific version number
    subprocess.run(["docker", "build", "-t", f"source:{version}", "./temp_repo"])
    
    # Tag the Docker image with your Docker Hub username and repository
    subprocess.run(["docker", "tag", f"source:{version}", f"{DOCKER_USERNAME}/source:{version}"])
    
    # Push the Docker image to Docker Hub
    subprocess.run(["docker", "push", f"{DOCKER_USERNAME}/source:{version}"])
    
    # Clean up the temporary repository folder
    subprocess.run(["rm", "-rf", "./temp_repo"])

import os
import platform
import shutil
import subprocess
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Declare a dictionary of version numbers and their corresponding git SHAs
version_and_sha = {
    'v1.0': 'bfeb478a55240c332a8e6b28e689d549e10ddbec', 
    'v2.0': '09dbbb257084cc837dc4661128da1b50de0ce537', 
    'v3.0': '979083872ce1eb107974e36e3d8f3fdbd2de88d0'
    }

DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")

GIT_ACCESS_TOKEN = os.getenv("GIT_ACCESS_TOKEN")
GIT_REPOSITORY = os.getenv("GIT_REPOSITORY")

IMAGE_NAME = "python_build_image"

for version, sha in version_and_sha.items():
    # Clone the specific version of the repository
    subprocess.run(["git", "clone", f"https://{GIT_ACCESS_TOKEN}@{GIT_REPOSITORY}", "./temp_repo"])
    # subprocess.run(["git", "clone", f"https://{GIT_ACCESS_TOKEN}@{GIT_REPOSITORY}", "--branch", sha, "./temp_repo"])

    # Build the Docker image with the specific version number
    subprocess.run(["docker", "build", "-t", f"{IMAGE_NAME}:{version}", "./temp_repo"])
    
    # Tag the Docker image with your Docker Hub username and repository
    subprocess.run(["docker", "tag", f"{IMAGE_NAME}:{version}", f"{DOCKER_USERNAME}/{IMAGE_NAME}:{version}"])
    
    # Push the Docker image to Docker Hub
    subprocess.run(["docker", "push", f"{DOCKER_USERNAME}/{IMAGE_NAME}:{version}"])
    
    # Clean up the temporary repository 
    if platform.system() == "Windows":
        # Use the rmdir command on Windows
        command = f'rmdir /s /q "./temp_repo"'
    else:
        # Use the rm command on other systems
        command = f'rm -rf "./temp_repo"'
    subprocess.call(command, shell=True)
    break


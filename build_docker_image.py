import os
import platform
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Declare a dictionary of version numbers and their corresponding git SHAs
version_and_sha = {
    "1.0": "bfeb478a55240c332a8e6b28e689d549e10ddbec",
    "2.0": "8153df2c37bcea4a4beeb090851903150d7f1633",
    "3.0": "da634bf2c1e6bbfb36cc3172966ede6c9a8c7dc8"
}

DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")

GIT_ACCESS_TOKEN = os.getenv("GIT_ACCESS_TOKEN")
GIT_REPOSITORY = os.getenv("GIT_REPOSITORY")

IMAGE_NAME = os.getenv("IMAGE_NAME")

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

    print(f"Version {version} successfully pushed to Docker")
    
    # Clean up the temporary repository 
    if platform.system() == "Windows":
        # Use the rmdir command on Windows
        command = f'rmdir /s /q "./temp_repo"'
    else:
        # Use the rm command on other systems
        command = f'rm -rf "./temp_repo"'
    subprocess.call(command, shell=True)
    break
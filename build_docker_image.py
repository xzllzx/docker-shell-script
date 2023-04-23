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
TEMP_REPO = "./temp_repo"

def remove_temp_repo(folder_path):
    folder_path = os.path.normpath(folder_path)
    # Clean up the temporary repository 
    if platform.system() == "Windows":
        # Use the rmdir command on Windows
        command = f'rmdir /s /q {folder_path}'
    else:
        # Use the rm command on other systems
        command = f'rm -rf {folder_path}'
    subprocess.call(command, shell=True)

def main():
    if os.path.exists(TEMP_REPO):
        print(f"Removing existing {TEMP_REPO}")
        remove_temp_repo(TEMP_REPO)

    os.makedirs(TEMP_REPO, exist_ok=True)
    os.chdir(TEMP_REPO)

    # Clone the repository
    subprocess.run(["git", "clone", f"https://{GIT_ACCESS_TOKEN}@{GIT_REPOSITORY}", "."])

    for version, sha in version_and_sha.items():
        # Checkout the specific version
        subprocess.run(["git", "checkout", sha])

        # Build the Docker image with the specific version number
        subprocess.run(["docker", "build", "-t", f"{IMAGE_NAME}:{version}", "."])
        
        # Tag the Docker image with your Docker Hub username and repository
        subprocess.run(["docker", "tag", f"{IMAGE_NAME}:{version}", f"{DOCKER_USERNAME}/{IMAGE_NAME}:{version}"])
        
        # Push the Docker image to Docker Hub
        subprocess.run(["docker", "push", f"{DOCKER_USERNAME}/{IMAGE_NAME}:{version}"])

        print(f"Version {version} successfully pushed to Docker")
        
    # Clean up the temporary repository folder
    os.chdir("../")

    remove_temp_repo(TEMP_REPO)

if __name__ == "__main__":
    main()
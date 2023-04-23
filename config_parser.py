import configparser
import json
from pathlib import Path

def parse_config_file(config_file_path: Path, format: str) -> dict[str, str]:
    format_lower = format.lower()
    # Create a ConfigParser object and read the configuration file
    config = configparser.ConfigParser()
    config.read(config_file_path)


    # Loop over all sections and options in the configuration file
    if format_lower == 'python':
        # Create a dictionary to store the key-value pairs
        result = {}
        for section in config.sections():
            for option in config.options(section):
                # Add the key-value pair to the dictionary
                result[f"{option}"] = config.get(section, option)
        print(f"version_and_sha = {json.dumps(result, indent=4)}")

    elif format_lower == 'bash':
        # Initialize a list to store the version and SHA information
        result = []
        # Loop through the sections in the config file (should only be the "git" section)
        for section in config.sections():
            # Loop through the options in the section (should be the version numbers and SHA keys)
            for option in config.options(section):
                # Extract the version number and SHA key
                version = option
                sha = config.get(section, option)

                # Format the output and add it to the list
                result.append(f'    ["{version}"]="{sha}",')
        result = '\n'.join(result)
        result = f"declare -A version_and_sha=(\n{result}\n)"
        print(result)

if __name__ == '__main__':
    config_filepath = Path('config.ini')
    parse_config_file(config_filepath, format='bash')
    parse_config_file(config_filepath, format='python')
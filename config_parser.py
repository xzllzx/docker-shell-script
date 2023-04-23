import configparser
from pathlib import Path

def parse_config_file(config_file_path: Path) -> dict[str, str]:
    # Create a ConfigParser object and read the configuration file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Create a dictionary to store the key-value pairs
    result = {}

    # Loop over all sections and options in the configuration file
    for section in config.sections():
        for option in config.options(section):
            # Add the key-value pair to the dictionary
            result[f"{option}"] = config.get(section, option)

    return result

if __name__ == '__main__':
    config_filepath = Path('config.ini')
    x = parse_config_file(config_filepath)
    print(x)
import configparser
from modules.customLogger import setup_logger
# from customLogger import setup_logger


logger = setup_logger()

CONFIG_PATH = r".\config.ini"
# CONFIG_PATH = r"H:\UE_Projects_H\EchoWhisperTemplate\EchoWhisperAPI\config.ini"

def load_config(file_path):
    """
    Load and read the configuration file.
    :param file_path: Path to the config.ini file.
    :return: ConfigParser object with the loaded configuration.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    logger.debug("Loaded configuration from %s", file_path)
    return config

def get_config_value(config, section, key, default=None):
    """
    Get the value of a specific key from a specified section in the configuration.
    :param config: ConfigParser object.
    :param section: Section name in the config file.
    :param key: Key whose value is to be fetched.
    :param default: Default value to return if the key or section is not found.
    :return: Value of the specified key, or the default value if not found.
    """
    try:
        logger.debug("Getting value for key '%s' from section '%s'", key, section)
        return config[section][key]
    except KeyError:
        logger.error("Key '%s' not found in section '%s'. Using default value of '%s'.", key, section, default)
        return default
    
def get_config_object():
    return load_config(CONFIG_PATH)

if __name__ == "__main__":
    config = get_config_object()
    print(config.sections())
    print(config["Vector Store"]["FOLDERPATH"])
    print(get_config_value(config, "Vector Store", "FOLDERPATH"))
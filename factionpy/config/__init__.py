import os
import json
from factionpy.logger import log

global_config = os.environ.get("FACTION_CONFIG_PATH", "/opt/faction/global/config.json")
local_config = "./config.json"


def get_config_value(value):
    config_file_path = global_config

    if os.path.exists(local_config):
        config_file_path = local_config

    if os.path.exists(config_file_path):
        try:
            with open(config_file_path) as f:
                config = json.load(f)
            return config.get(value)
        except Exception as e:
            log("config.py", f"Error: {str(e)} - {str(type(e))}")
            log("config.py", "Could not load config file: {0}".format(config_file_path))
            return None
    else:
        try:
            return os.environ.get(value)
        except KeyError as e:
            log("config.py", "Config value not  in environment: {0}".format(str(e)))
            return None
        except Exception as e:
            log("config.py", "Unknown error: {0}".format(str(e)))
            return None

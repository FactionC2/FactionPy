import os
import json
from factionpy.logger import log

global_config = os.environ.get("FACTION_CONFIG_PATH", "/opt/faction/global/config.json")
local_config = "./config.json"


def get_config():
    config_file_path = local_config

    if os.path.exists(global_config):
        config_file_path = global_config

    if os.path.exists(config_file_path):
        try:
            with open(config_file_path) as f:
                config = json.load(f)
            return config
        except Exception as e:
            log("config.py", f"Error: {str(e)} - {str(type(e))}")
            log("config.py", "Could not load config file: {0}".format(config_file_path))
            exit(1)
    else:
        try:
            config = dict()
            config["FLASK_SECRET"] = os.environ["FLASK_SECRET"]
            config["POSTGRES_DATABASE"] = os.environ["POSTGRES_DATABASE"]
            config["POSTGRES_USERNAME"] = os.environ["POSTGRES_USERNAME"]
            config["POSTGRES_PASSWORD"] = os.environ["POSTGRES_PASSWORD"]
            config["POSTGRES_HOST"] = os.environ["POSTGRES_HOST"]
            config["ADMIN_PASSWORD"] = os.environ["ADMIN_PASSWORD"]
            config["SYSTEM_PASSWORD"] = os.environ["SYSTEM_PASSWORD"]
            return config
        except KeyError as e:
            log("config.py", "Config value not  in environment: {0}".format(str(e)))
            exit(1)
        except Exception as e:
            log("config.py", "Unknown error: {0}".format(str(e)))
            exit(1)


def get_config_value(name):
    try:
        config = get_config()
        return config[name]
    except Exception as e:
        log("factionpy:get_config_value", "Could not load value for {0} from config. Error: {1}".format(name, str(e)), "debug")
        return None

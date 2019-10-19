import os
import json
from factionpy.logger import log

config_file_path = "/opt/faction/global/config.json"


def get_config():
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path) as f:
                config = json.load(f)
            return config
        except Exception as e:
            log("config.py", f"Error: {str(e)} - {str(type(e))}", "debug")
            log("config.py", "Could not load config file: {0}".format(config_file_path), "debug")
    else:
        try:
            config = dict()
            config["API_UPLOAD_DIR"] = os.environ["API_UPLOAD_DIR"]
            config["FLASK_SECRET"] = os.environ["FLASK_SECRET"]
            config["POSTGRES_DATABASE"] = os.environ["POSTGRES_DATABASE"]
            config["POSTGRES_USERNAME"] = os.environ["POSTGRES_USERNAME"]
            config["POSTGRES_PASSWORD"] = os.environ["POSTGRES_PASSWORD"]
            config["POSTGRES_HOST"] = os.environ["POSTGRES_HOST"]
            config["RABBIT_USERNAME"] = os.environ["RABBIT_USERNAME"]
            config["RABBIT_PASSWORD"] = os.environ["RABBIT_PASSWORD"]
            config["RABBIT_HOST"] = os.environ["RABBIT_HOST"]
            config["MINIO_ACCESSKEY"] = os.environ["MINIO_ACCESSKEY"]
            config["MINIO_SECRETKEY"] = os.environ["MINIO_SECRETKEY"]
            return config
        except KeyError as e:
            log("config.py", "Config value not  in environment: {0}".format(str(e)), "debug")
        except Exception as e:
            log("config.py", "Unknown error: {0}".format(str(e)), "debug")


def get_config_value(name):
    try:
        config = get_config()
        return config[name]
    except Exception as e:
        log("factionpy:get_config_value", "Could not load value for {0} from config. Error: {1}".format(name, str(e)), "debug")
        return None

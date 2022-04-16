import yaml
import logging
from functools import lru_cache

@lru_cache()
def parsing_yaml():
    with open("./settings.yaml", 'rb') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.info(exc)
        finally:
            return parsed_yaml

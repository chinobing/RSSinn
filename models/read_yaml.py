import yaml
import logging

def parsing_yaml():
    with open("./settings.yaml", 'rb') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.info(exc)
        finally:
            print(parsed_yaml)
            return parsed_yaml

"""General purpose utilities for Sysdig.

Following are the utilities:

- Create the logging object
- Read the YAML configurations
- Dump the received data in json file.
"""

import json
import logging
from logging import Logger
from typing import Dict

import yaml  # type: ignore


def set_logger(log_filename: str = "", log_format: str = "") -> Logger:
    """Set the configurations for logger.

    :param log_filename: Filename in which logs are logged, defaults to ""
    :type log_filename: str, optional
    :param log_format: Log format, defaults to ""
    :type log_format: str, optional
    :return: Configured logging object
    :rtype: Logger
    """
    if not log_filename:
        log_filename = "SecureEvents_connector.log"

    if not log_format:
        log_format = "%(asctime)s %(name)s %(levelname)s: [In %(filename)s at line %(lineno)d] | %(message)s"

    logging.basicConfig(format=log_format, filename=log_filename, level=logging.INFO)

    return logging.getLogger(log_filename)


def read_yaml(yaml_file: str) -> Dict:
    """Read Yaml file and return the data as dictionary.

    :param yaml_file: Yaml file name along with the path
    :type yaml_file: str
    :return: Data in Yaml file
    :rtype: Dict
    """
    data: Dict = {}
    # Open the file and load the file
    with open(yaml_file, encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data


def dump_data(json_file: str, data: Dict) -> None:
    """Dump the data into the JSON file.

    :param json_file: Json file name along with path
    :type json_file: str
    :param data: Data to be dumped
    :type data: Dict
    """
    with open(f"{json_file}.json", "w", encoding="utf-8") as outfile:
        json.dump(data, outfile)

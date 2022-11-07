"""SysDig Connector module.

SysDig Plugin Connector performs the following actions:
- Initialize the logging module
- Read the configs file and get the required configurations
- Initialize the ResponseData object with its necessary configurations
- Collects and stores the Secure Event's and Audit Event's data in local device.
"""

import sys

from secureEvents_connector.controller.data import ResponseData
from secureEvents_connector.utils.general import read_yaml, set_logger

if __name__ == "__main__":

    LOG_FILENAME = "secureEvents_connector.log"
    # Get the logger object
    logger = set_logger(LOG_FILENAME)

    CONFIGS_FILEPATH = sys.argv[1]

    logger.info(f"Reading the config file : {CONFIGS_FILEPATH}")
    configs = read_yaml(CONFIGS_FILEPATH)
    logger.info(f"Got the configs from {CONFIGS_FILEPATH}")

    base_url: str = configs["secureEvents_connector"]["base_url"]
    filename: str = configs["secureEvents_connector"]["store_filename"]
    access_token = configs["secureEvents_connector"]["access_token"]
    response = ResponseData(
        access_token,
        base_url=base_url,
        start_time=configs["secureEvents_connector"]["from"],
        end_time=configs["secureEvents_connector"]["to"],
        logger=logger,
    )

    logger.info("Starting to get list of SecureEvents")
    SecureEvents_connector_count = response.get_secure_events_count(filename=filename)
    logger.info(f"Got the Secure events count which is {SecureEvents_connector_count}")

    logger.info("Starting to get list of audit activity events")
    activityaudit_count = response.get_activityaudit_events_count(filename=filename)
    logger.info(f"Got the audit activity events count which is {activityaudit_count}")

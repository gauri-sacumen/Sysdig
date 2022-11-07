# Sysdig Secure connector

This Connector fetch's the SecureEvents data and Audit Events data from the Sysdig Platform and stores the data locally in a JSON file.

## Steps to run the connector

- Step 1: Install the virtual environment using the following command in the command prompt/terminal:

      `python -m venv <virtual_env_name>`
p
- Step 2: Enable a virtual environment.
  - For Windows:  Use the below command (without the word source) in the command prompt to activate the virtual environment.

        `venv\Scripts\activate`

  - For Linux/Mac/Ubuntu:  Use the below command in the terminal to activate the virtual environment.

        `source venv\bin\activate`

- Step 3: Install the required libraries by executing the below command.

      `pip install -r requirements.txt`

- Step 4: Configurations.
  - Provide the access token, Sysdig URL, limit,start timestamp,end timestamp and store_filename in `configs.yaml` file.

- Step 5: Execute the below command in the terminal to set up the python environment for the execution of the connector.

      `python setup.py develop`

- Step 6: Execute the below command in the terminal to start the connector.

      `python connector.py configs.yaml`


 ## How to provide the required file base_url,access_token,from,to and store_filename in the configs.yaml file.
```yaml
SecureEvents_connector :
  base_url :
  access_token :
  from :
  to :
  store_filename :

### Example
Note:
from is start date in nanosecods
to is end date in nanosecods

SecureEvents_connector :
  base_url :
  access_token :
  from : 1666675800000000000
  to : 1667367000000000000
  store_filename : SecureEvents_connector

```

## Sysdig Plugin connector.py file.
This performs the following actions:
- Initialize the logging module
- Read the configs file and get the required configurations
- Initialize the ResponseData object with its necessary configurations
- Collects and stores the event's data in the local device.

## Sysdig Plugin Controller Module

### controller.auth
- It provides an access token to access the APIs.

### controller.client
- Helps in making normal requests and paginated requests with SecureEvents_connector APIs.
- Paginated request's responses are stored in a JSON file in the local connector directory of the device.

### controller.data
- Provides the access token
- Get the Secure events and audit events data
- Store the responses in respective files and get the count of the responses.

## Sysdig Plugin Utils Module

### utils.general
General purpose utilities for Sysdig Plugin.
Following are the utilities:

- Create the logging object.
- Read the YAML configurations.
- Dump the received data in a JSON file.

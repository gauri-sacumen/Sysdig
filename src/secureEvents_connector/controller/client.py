"""Sysdig SecureEvents_connector Plugin Connect.

Helps in making normal requests and paginated requests with Sysdig APIs.
Paginated request's responses are stored in a JSON file in the local connector directory of the device.
"""
import time
from logging import Logger
from typing import Any, Dict, List, Optional, Union

import requests  # type: ignore
from requests import Response

from secureEvents_connector.utils.general import dump_data


class Connect:
    """Connect with the uri and get the response.

    :raises TypeError: If Response is a list
    :raises SystemExit: Response timed out
    :raises SystemExit: HTTP error received in the response
    :raises SystemExit: Connection error received in the response
    :raises SystemExit: Some error received in the response
    """

    RETRY_CODES = [429, 500, 502, 503, 504]

    def __init__(
        self,
        access_token: str = "",
        max_retries: int = 3,
        start_time: str = "",
        end_time: str = "",
        limit: int = 10,
        logger: Optional[Logger] = None,
    ) -> None:
        """Initialise the connection.

        :param access_token: Access token to be used to authenticate the request
        :type access_token: str
        :param max_retries: Number of retries, defaults to 3
        :type max_retries: int, optional
        :param start_time: Start time is initial timestamp given for the request
        :type start_time: str
        :param end_time: End time is end timestamp given for the request
        :type end_time: str
        :param limit: Total number of items to fetch in one page, defaults to 1000
        :type limit: int, optional
        """
        self.access_token = access_token  # nosec
        self.max_retries = max_retries
        self.start_time = start_time
        self.end_time = end_time
        self.api_call_count = 0
        self.limit = limit

        self.logger = logger

    def paginated_request(
        self,
        method: str,
        uri: str,
        params: Optional[Dict] = None,
        data: Optional[Union[List, Dict, str]] = None,
        **kwargs: Any,
    ) -> int:
        """Make paginated requests to the APIs.

        :param method: HTTP method
        :type method: str
        :param uri: URL for One Login API endpoint to connect
        :type uri: str
        :param params: Paramters for Http request, defaults to None
        :type params: Optional[Dict], optional
        :param data: Payload data for Http request, defaults to None
        :type data: Optional[Union[List, Dict, str]], optional
        :raises TypeError: If response is a list.
        :return: Count of the total response data
        :rtype: int
        """
        params = params or {}

        params["from"] = self.start_time
        params["to"] = self.end_time
        params["limit"] = self.limit

        self.logger.debug(f"Pagination Start date : {params['from']}")  # type: ignore
        self.logger.debug(f"Pagination End date : {params['to']}")  # type: ignore

        if self.access_token is None:
            raise AttributeError("No access token")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        page_count = 0
        record_count = 0

        filename = kwargs.get("filename", "./sample")
        del kwargs["filename"]

        status = True
        while status:
            page_count += 1
            print(page_count)
            print(uri)
            result = self.send(
                method, uri, params=params, headers=headers, data=data, **kwargs
            )
            self.logger.info("Got the response")  # type: ignore
            response = result.json()
            self.logger.debug("Response = {response}")  # type: ignore
            if isinstance(response, list):
                raise TypeError("Invalid Response")
            res_data = response.get("data", None)
            # TODO : Should be replaced by the call to client apis  pylint: disable=fixme
            file_name = f"{filename}_{page_count}"
            self.logger.info(f"Dumping the response in file {file_name}")  # type: ignore
            dump_data(file_name, res_data)
            self.logger.info("Finished Dumping the response")  # type: ignore
            record_count += len(res_data)

            status = bool(response.get("page", {}).get("next", None))
            if status:
                # Use a new URI from the link header for the next page
                if "from" and "to" in params.keys():
                    del params["from"]
                    del params["to"]
                params["cursor"] = response["page"]["next"]
                print(params["cursor"])
                self.logger.info("Got the next page cursor")  # type: ignore

        return record_count

    def send(
        self,
        method: str,
        uri: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        data: Optional[Union[List, Dict, str]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send request to the Sysdig APIs.

        :param method: HTTP method
        :type method: str
        :param uri: URL for One Login API endpoint to connect
        :type uri: str
        :param params: Query paramters for Http request, defaults to None
        :type params: Optional[Dict], optional
        :param headers: Request Header for making API request, defaults to None
        :type headers: Optional[Dict], optional
        :param data: Payload data for Http request, defaults to None
        :type data: Optional[Union[List, Dict, str]], optional
        :raises SystemExit: Request Timed out
        :raises SystemExit: Http Error received
        :raises SystemExit: Connection error received
        :raises SystemExit: Some other requests error received
        :return: API request's response
        :rtype: Response
        """
        response: Any = None
        request_count = 0

        request_kwargs: Dict[str, Any] = {
            "params": params or {},
            "headers": headers or {},
            **kwargs,
        }

        if data is not None:
            request_kwargs["data"] = data

        # Total requests = 1st request + max retries
        while request_count <= self.max_retries:

            request_count += 1

            try:
                response = requests.request(method, uri, **request_kwargs)
                self.api_call_count += 1
                response.raise_for_status()

            except requests.exceptions.Timeout as err:
                # If there are still tries left, and status code might be solved with a retry,
                #   then try again after sleeping.  Max retries + 1st try.
                must_retry = response.status_code in self.RETRY_CODES
                can_retry = request_count < (self.max_retries + 1)
                if must_retry and can_retry:
                    time.sleep(2**request_count)
                else:
                    # Remove query params so we're not logging unnecessary customer-related data
                    url = str(err.request.url).split("?", maxsplit=1)[0]
                    msg = f"Status code {err.response.status_code} for {url} on try {request_count} of {self.max_retries + 1} allowed tries"
                    self.logger.error(msg)  # type: ignore
                    raise SystemExit(msg, err) from err

            except requests.exceptions.HTTPError as err:
                self.logger.error(f"Received {err.__class__.__name__}: ", err)  # type: ignore
                raise SystemExit(f"Received {err.__class__.__name__}", err) from err
            except requests.exceptions.ConnectionError as err:
                self.logger.error(f"Received {err.__class__.__name__}: ", err)  # type: ignore
                raise SystemExit(f"Received {err.__class__.__name__}", err) from err
            except requests.exceptions.RequestException as err:
                self.logger.error(f"Received {err.__class__.__name__}: ", err)  # type: ignore
                raise SystemExit(f"Received {err.__class__.__name__}", err) from err

        return response

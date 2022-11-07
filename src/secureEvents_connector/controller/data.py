"""Sysdig Plugin ResponseData.

Helps to retrieve the response from SecureEvents_connector APIs.
Following are actions it performs:

- Get list of events
- Store the responses in respective files and get the count of the responses.
"""
from logging import Logger
from typing import Optional

from secureEvents_connector.controller.client import Connect


class ResponseData:
    """Used to call the API's with necessary details and get the response count."""

    def __init__(
        self,
        access_token: str,
        base_url: str,
        start_time: str,
        end_time: str,
        limit: int = 10,
        logger: Optional[Logger] = None,
    ) -> None:
        """Initialize the ResponseData class.

        :param access_token: Access token of the Sysdig Application
        :type access_token: str
        :param base_url: Base URL of the Sysdig application
        :type base_url: str
        :param start_time: Start Timestamp of the Sysdig Application
        :type start_time: str
        :param end_time: End Timestamp of the Sysdig Application
        :type end_time: str
        :param logger: Logger object, defaults to None
        :type logger: Optional[Logger], optional
        """
        self.access_token = access_token
        self.base_url = base_url
        self.start_time = start_time
        self.end_time = end_time
        self.logger = logger
        self.limit = limit
        self.api_call_count = 0

    def get_response(self, uri: str, filename: str) -> int:
        """Get the response from the API's and store the count in the file.

        :param uri: URL for One Login API endpoint to connect
        :type uri: str
        :param filename: Name of the file in which response data is stored
        :type filename: str
        :return: Returns the count of the response data
        :rtype: int
        """
        client = Connect(
            access_token=self.access_token,
            start_time=self.start_time,
            end_time=self.end_time,
            limit=self.limit,
            logger=self.logger,
        )
        return client.paginated_request("get", uri, filename=filename)

    def get_secure_events_count(self, filename: str = "") -> int:
        """Get the list of events by providing the list_events endpoint and list_events file name.

        :param filename: Filename in which to store the users count
        :return: Count of the list_events data
        :rtype: int
        """
        secure_events_uri = f"{self.base_url}api/v1/secureEvents"
        self.logger.info(secure_events_uri)  # type: ignore
        secure_events_filename = (
            f"{filename}_list_events" if filename else "list_events"
        )

        return self.get_response(secure_events_uri, secure_events_filename)

    def get_activityaudit_events_count(self, filename: str = "") -> int:
        """Get the list of audit events data by providing the audit_events endpoint and audit_events file name.

        :param filename: Filename in which to store the events count
        :return: Count of the audit_events data
        :rtype: int
        """
        audit_events_uri = f"{self.base_url}api/v1/activityAudit/events"
        audit_events_filename = (
            f"{filename}_audit_events" if filename else "audit_events"
        )

        return self.get_response(audit_events_uri, audit_events_filename)

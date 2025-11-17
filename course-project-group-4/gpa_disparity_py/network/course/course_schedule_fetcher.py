from enum import Enum
import resource
from urllib import request
from xml.dom import xmlbuilder
import requests
from urllib.parse import urlencode
import xmltodict
import json
from definitions import TEST_FILE_PATH


class Semester(Enum):
    """Enum to select season of semester

    Args:
        Enum (str): _description_
    """

    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


class DetailMode(Enum):
    """optional parameter that allows the client to specify the level of
    detail to return for any specific object document

    Args:
        Enum (str): parameter
    """

    LINKS = "links"
    SUMMARY = "summary"
    DETAIL = "detail"
    CASCADE = "cascade"


class BaseUrl(Enum):
    SCHEDULE = "http://courses.illinois.edu/cisapp/explorer/schedule"
    CATALOG = "https://courses.illinois.edu/cisapp/explorer/catalog"


class ApiPathConfig:
    """Class used for configuring API request path fields"""

    def __init__(
        self,
        year=None,
        semester=None,
        subject_code=None,
        course_number=None,
        crn=None,
    ):
        """constructor

        Args:
            year (int, optional): Defaults to None.
            semester (Semester, optional): Defaults to None.
            subject_code (str, optional): Defaults to None.
            course_number (int, optional): Defaults to None.
            crn (int, optional): Defaults to None.
        """
        self.year = year
        self.semester = semester.lower() if semester else None
        self.subject_code = subject_code.upper() if subject_code else None
        self.course_number = course_number
        self.crn = crn


class CourseScheduleFetcher:
    def _set_mode(self, query_params: dict = {}, mode: DetailMode = DetailMode.SUMMARY):
        """changes the mode of the API query parameter to 'links'

        Args:
            query_params (dict): the query parameters dictionary to be passed to
                                http://courses.illinois.edu/cisapp/explorer
        """
        query_params["mode"] = mode.value
        return query_params

    def _build_illinois_link(
        self, base_url: BaseUrl, api_path_config: ApiPathConfig, query_params: dict
    ) -> str:
        """Build API links for http://courses.illinois.edu/cisapp/explorer.
            Can poll schedule / course info.
            See documentation https://courses.illinois.edu/cisdocs/explorer
        Args:
            api_path_config (ApiPathConfig): class used to configure the API request
            query_params (dict): the query parameters dictionary ()

        Returns:
            str: URL for the API requests
        """
        # year=None, semester=None, subject_code=None, course_number=None, crn=None

        if type(base_url) == type(BaseUrl):
            base_url = base_url.value

        path_parts = [
            api_path_config.year,
            api_path_config.semester,
            api_path_config.subject_code,
            api_path_config.course_number,
            api_path_config.crn,
        ]

        for part in path_parts:
            if part:
                base_url += f"/{part}"
            else:
                break  # terminates when None is encountered

        base_url += ".xml"

        return base_url

    # TODO - make network operations async

    def _get_webpage(self, url: str, header: dict):
        """Fetches webpage

        Args:
            url (str): url to webpage
            header (dict): json dictionary

        Returns:
            _type_: _description_
        """
        web_request = request.Request(url, headers=header)
        resource = request.urlopen(web_request)

        return resource

    def _format_webpage(self, resource):
        # processes resource for use in _class_csv_to_json
        resource = resource.read().decode("utf-8-sig")
        # resource = resource.splitlines()
        return resource

    @classmethod
    def _xml_to_dict(self, data_source):
        """Converts xml input to json
        based on: https://www.geeksforgeeks.org/python-xml-to-json/

        Args:
            resource (_type_): file pointer or formatted webpage

        Returns:
            _type_: _description_
        """
        data_dict = xmltodict.parse(data_source)

        return data_dict

    def get_course_schedule(
        self, base_url: BaseUrl, api_path_config: ApiPathConfig, query_params: dict
    ):
        url = self._build_illinois_link(base_url, api_path_config, query_params)
        webpage = self._get_webpage(url)
        formatted_page = self._format_webpage(webpage)
        data_dict = self._xml_to_dict(formatted_page)
        return data_dict

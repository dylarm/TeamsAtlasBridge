import logging
from typing import Tuple, NewType

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from constants import VERSION as CURRENT_VERSION

logger = logging.getLogger(__name__)


Version = NewType("Version", Tuple[int, ...])


def get_latest_ver(
    url: str = "https://api.github.com/repos/dylarm/TeamsAtlasBridge/releases/latest"
) -> Tuple[Version, str]:
    latest_version: Version = Version(
        (0, 0, 0)
    )  # Will always cause version check to be false if not updated
    latest_url: str = ""
    try:
        response = requests.get(url)
        response.raise_for_status()  # For any HTTP Errors
        latest_version = Version(
            tuple(int(x) for x in response.json()["tag_name"].lstrip("v").split("."))
        )
        latest_url = response.json()["html_url"]
    except HTTPError as e:
        logger.warning(f"A HTTP Status error occurred while checking for updates:\n{e}")
    except (ConnectionError, Timeout) as e:
        logger.warning(f"A Connection error occurred while checking for updates:\n{e}")
    except RequestException as e:
        logger.warning(
            f"A potentially serious error occurred while checking for updates:\n{e}"
        )
    return latest_version, latest_url


def update_available(
    current_ver: str = CURRENT_VERSION, latest_ver: Version = get_latest_ver()[0]
) -> bool:
    current_ver_tuple = tuple(int(x) for x in current_ver.lstrip("v").split("."))
    return latest_ver > current_ver_tuple

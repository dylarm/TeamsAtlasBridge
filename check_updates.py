import logging
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from typing import Tuple

from constants import VERSION as CURRENT_VERSION

logger = logging.getLogger(__name__)


def get_latest_ver(
    url: str = "https://api.github.com/repos/dylarm/TeamsAtlasBridge/releases/latest"
) -> Tuple[str, str]:
    latest_version: str = "z"  # Will always be the "greatest" version possible
    latest_url: str = ""
    try:
        response = requests.get(url)
        response.raise_for_status()  # For any HTTP Errors
        latest_version = response.json()["tag_name"]
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
    current_ver: str = CURRENT_VERSION, latest_ver: str = get_latest_ver()[0]
) -> bool:
    return latest_ver > current_ver

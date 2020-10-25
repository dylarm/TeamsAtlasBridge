import logging
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from constants import VERSION as CURRENT_VERSION

logger = logging.getLogger(__name__)


def get_latest_ver(
    url: str = "https://api.github.com/repos/dylarm/TeamsAtlasBridge/releases/latest"
) -> str:
    latest_version: str = "z"  # Will always be the "greatest" version possible
    try:
        response = requests.get(url)
        response.raise_for_status()  # For any HTTP Errors
        latest_version = response.json()["tag_name"]
    except HTTPError as e:
        logger.warning(f"A HTTP Status error occurred while checking for updates:\n{e}")
    except (ConnectionError, Timeout) as e:
        logger.warning(f"A Connection error occurred while checking for updates:\n{e}")
    except RequestException as e:
        logger.warning(
            f"A potentially serious error occurred while checking for updates:\n{e}"
        )
    return latest_version


def update_available(
    current_ver: str = CURRENT_VERSION, latest_ver: str = get_latest_ver()
) -> bool:
    return latest_ver > current_ver

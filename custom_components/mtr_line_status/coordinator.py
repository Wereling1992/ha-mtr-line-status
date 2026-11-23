"""DataUpdateCoordinator for MTR Line Status."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LINES, STATUS_URL

_LOGGER = logging.getLogger(__name__)


class MTRDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching MTR line status data."""

    def __init__(self, hass: HomeAssistant, scan_interval: int) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from MTR."""
        try:
            async with self._session.get(
                STATUS_URL,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error fetching data: HTTP {response.status}")
                text = await response.text()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with MTR: {err}") from err

        return self._parse_status(text)

    def _parse_status(self, text: str) -> dict[str, Any]:
        """Parse the XML status into a structured dict."""
        result: dict[str, Any] = {
            "last_update": None,
            "lines": {},
        }

        try:
            root = ET.fromstring(text)
        except ET.ParseError as err:
            _LOGGER.error("Failed to parse MTR XML: %s", err)
            for code, (name_en, name_zh, color) in LINES.items():
                result["lines"][code] = {
                    "status": "unknown",
                    "color": color,
                    "name_en": name_en,
                    "name_zh": name_zh,
                }
            return result

        last_build = root.find("lastBuildDate")
        if last_build is not None and last_build.text:
            result["last_update"] = last_build.text.strip()

        for line_elem in root.findall("line"):
            code_elem = line_elem.find("line_code")
            if code_elem is None or not code_elem.text:
                continue

            code = code_elem.text.strip()
            if code not in LINES:
                continue

            status_elem = line_elem.find("status")
            status = (
                status_elem.text.strip().lower()
                if status_elem is not None and status_elem.text
                else "unknown"
            )

            color_elem = line_elem.find("line_color")
            color = (
                color_elem.text.strip()
                if color_elem is not None and color_elem.text
                else LINES[code][2]
            )

            name_en_elem = line_elem.find("line_name")
            name_zh_elem = line_elem.find("line_name_tc")

            result["lines"][code] = {
                "status": status,
                "color": color,
                "name_en": (
                    name_en_elem.text.strip()
                    if name_en_elem is not None and name_en_elem.text
                    else LINES[code][0]
                ),
                "name_zh": (
                    name_zh_elem.text.strip()
                    if name_zh_elem is not None and name_zh_elem.text
                    else LINES[code][1]
                ),
            }

        for code, (name_en, name_zh, color) in LINES.items():
            if code not in result["lines"]:
                result["lines"][code] = {
                    "status": "unknown",
                    "color": color,
                    "name_en": name_en,
                    "name_zh": name_zh,
                }

        return result

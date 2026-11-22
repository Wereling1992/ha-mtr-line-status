"""DataUpdateCoordinator for MTR Line Status."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
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

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from MTR."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(STATUS_URL, timeout=10) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    text = await response.text()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with MTR: {err}") from err

        return self._parse_status(text)

    def _parse_status(self, text: str) -> dict[str, Any]:
        """Parse the raw status text into a structured dict."""
        parts = text.strip().split()
        result: dict[str, Any] = {
            "last_update": None,
            "lines": {},
        }

        if not parts:
            return result

        # First two parts are usually the timestamp
        if len(parts) >= 2 and ":" in parts[1]:
            result["last_update"] = f"{parts[0]} {parts[1]}"
            data_parts = parts[2:]
        else:
            data_parts = parts

        i = 0
        while i < len(data_parts):
            code = data_parts[i]
            if code in LINES:
                # Expected format: CODE English_Name Chinese_Name #COLOR status
                status = "unknown"
                color = LINES[code][2]

                # Find the status (green / yellow / red)
                for j in range(i + 1, min(i + 8, len(data_parts))):
                    token = data_parts[j].lower()
                    if token in ("green", "yellow", "red"):
                        status = token
                        break
                    if token.startswith("#"):
                        color = token

                result["lines"][code] = {
                    "status": status,
                    "color": color,
                    "name_en": LINES[code][0],
                    "name_zh": LINES[code][1],
                }
                i += 1
            else:
                i += 1

        # Fill in any missing lines as unknown
        for code, (name_en, name_zh, color) in LINES.items():
            if code not in result["lines"]:
                result["lines"][code] = {
                    "status": "unknown",
                    "color": color,
                    "name_en": name_en,
                    "name_zh": name_zh,
                }

        return result

"""Sensor platform for MTR Line Status."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LINES
from .coordinator import MTRDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MTR Line Status sensors based on a config entry."""
    coordinator: MTRDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = [
        MTRLineSensor(coordinator, entry, code, name_en, name_zh, color)
        for code, (name_en, name_zh, color) in LINES.items()
    ]

    # lastBuildDate as a diagnostic sensor
    entities.append(MTRLastUpdateSensor(coordinator, entry))

    async_add_entities(entities)


def _device_info(entry: ConfigEntry) -> DeviceInfo:
    """Return the device info for the MTR integration."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="MTR Line Status",
        manufacturer="MTR Corporation",
        model="Line Status Feed",
        configuration_url="https://www.mtr.com.hk/alert/ryg_line_status_lite.xml",
    )


class MTRLineSensor(CoordinatorEntity[MTRDataUpdateCoordinator], SensorEntity):
    """Representation of a single MTR line status sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MTRDataUpdateCoordinator,
        entry: ConfigEntry,
        code: str,
        name_en: str,
        name_zh: str,
        color: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._code = code
        self._attr_unique_id = f"{entry.entry_id}_line_{code.lower()}"
        self._attr_name = f"{name_en} ({name_zh})"
        self._attr_icon = "mdi:subway"
        self._default_color = color
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        """Return the status of the line."""
        line_data = self.coordinator.data.get("lines", {}).get(self._code)
        if line_data:
            return line_data.get("status", "unknown")
        return "unknown"

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        line_data = self.coordinator.data.get("lines", {}).get(self._code, {})
        return {
            "line_code": self._code,
            "name_en": line_data.get("name_en"),
            "name_zh": line_data.get("name_zh"),
            "color": line_data.get("color", self._default_color),
        }

    @property
    def icon(self) -> str:
        """Return icon based on status."""
        status = self.native_value
        if status == "green":
            return "mdi:subway-variant"
        if status == "yellow":
            return "mdi:alert"
        if status == "red":
            return "mdi:close-octagon"
        return "mdi:subway"


class MTRLastUpdateSensor(CoordinatorEntity[MTRDataUpdateCoordinator], SensorEntity):
    """Sensor for the lastBuildDate from MTR feed."""

    _attr_has_entity_name = True
    _attr_name = "Last Update"
    _attr_icon = "mdi:clock-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MTRDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_last_update"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        """Return the last update timestamp from the feed."""
        return self.coordinator.data.get("last_update")

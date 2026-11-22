"""Sensor platform for MTR Line Status."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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

    entities = [
        MTRLineSensor(coordinator, code, name_en, name_zh, color)
        for code, (name_en, name_zh, color) in LINES.items()
    ]

    # Overall status sensor
    entities.append(MTROverallSensor(coordinator))

    async_add_entities(entities)


class MTRLineSensor(CoordinatorEntity[MTRDataUpdateCoordinator], SensorEntity):
    """Representation of a single MTR line status sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MTRDataUpdateCoordinator,
        code: str,
        name_en: str,
        name_zh: str,
        color: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._code = code
        self._attr_unique_id = f"mtr_line_{code.lower()}"
        self._attr_name = f"{name_en} ({name_zh})"
        self._attr_icon = "mdi:subway"
        self._default_color = color

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
            "last_update": self.coordinator.data.get("last_update"),
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


class MTROverallSensor(CoordinatorEntity[MTRDataUpdateCoordinator], SensorEntity):
    """Overall MTR network status sensor."""

    _attr_has_entity_name = True
    _attr_name = "Overall Status"
    _attr_unique_id = "mtr_overall_status"
    _attr_icon = "mdi:subway"

    def __init__(self, coordinator: MTRDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)

    @property
    def native_value(self) -> str:
        """Return overall status."""
        lines = self.coordinator.data.get("lines", {})
        statuses = [line.get("status") for line in lines.values()]

        if "red" in statuses:
            return "red"
        if "yellow" in statuses:
            return "yellow"
        if all(s == "green" for s in statuses):
            return "green"
        return "unknown"

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        lines = self.coordinator.data.get("lines", {})
        disrupted = [
            f"{data['name_zh']} ({code})"
            for code, data in lines.items()
            if data.get("status") in ("yellow", "red")
        ]
        return {
            "last_update": self.coordinator.data.get("last_update"),
            "disrupted_lines": disrupted,
            "disrupted_count": len(disrupted),
        }

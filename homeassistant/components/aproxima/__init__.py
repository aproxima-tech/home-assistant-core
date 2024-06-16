"""The Aproxima integration."""

from __future__ import annotations

from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized

from homeassistant.auth.models import User
from homeassistant.auth.permissions.const import POLICY_READ
from homeassistant.components.http import KEY_HASS, HomeAssistantView, require_admin
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONTENT_TYPE_JSON
import homeassistant.core as ha
from homeassistant.core import HomeAssistant
from homeassistant.helpers import (
    area_registry,
    device_registry,
    entity_registry,
    floor_registry,
)
from homeassistant.helpers.json import json_dumps


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Aproxima from a config entry."""
    hass.http.register_view(APIAreasView)
    hass.http.register_view(APIFloorsView)
    hass.http.register_view(APIDevicesView)
    hass.http.register_view(APIUsersView)

    return True


class APIAreasView(HomeAssistantView):
    """View to handle Areas requests."""

    url = "/api/aproxima/areas"
    name = "api:aproxima:areas"

    @ha.callback
    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Get current areas."""
        hass = request.app[KEY_HASS]
        ar = area_registry.async_get(hass)
        areas = (
            {"id": area.id, "name": area.name, "floorId": area.floor_id}
            for area in ar.async_list_areas()
        )
        return self.json(list(areas))


class APIFloorsView(HomeAssistantView):
    """View to handle Floors requests."""

    url = "/api/aproxima/floors"
    name = "api:aproxima:floors"

    @ha.callback
    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Get current floors."""
        hass = request.app[KEY_HASS]
        fr = floor_registry.async_get(hass)
        floors = (
            {"id": floor.floor_id, "name": floor.name, "level": floor.level}
            for floor in fr.async_list_floors()
        )
        return self.json(list(floors))


class APIDevicesView(HomeAssistantView):
    """View to handle Devices requests."""

    url = "/api/aproxima/devices"
    name = "api:aproxima:devices"

    @ha.callback
    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Get current devices."""
        hass = request.app[KEY_HASS]
        dr = device_registry.async_get(hass)
        devices = (
            {
                "id": device.id,
                "areaId": device.area_id,
                "name": device.name,
                "disabled": device.disabled,
                "type": device.entry_type,
                "model": device.model,
                "manufacturer": device.manufacturer,
                "serialNumber": device.serial_number,
            }
            for device in dr.devices.values()
        )
        return self.json(list(devices))


class APIUsersView(HomeAssistantView):
    """View to handle Users requests."""

    url = "/api/aproxima/users"
    name = "api:aproxima:users"

    @ha.callback
    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Get current users."""
        hass = request.app[KEY_HASS]
        users = await hass.auth.async_get_users()
        usersData = ({"id": user.id, "name": user.name} for user in users)
        return self.json(list(usersData))

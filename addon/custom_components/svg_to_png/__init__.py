import logging
import os
import requests
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("input_path"): cv.string,
        vol.Required("output_path"): cv.string,
    }
)

def setup(hass: HomeAssistant, config: ConfigType):
    """Set up the SVG to PNG service."""
    
    def handle_convert(call: ServiceCall):
        """Handle the conversion request."""
        input_path = call.data["input_path"]
        output_path = call.data["output_path"]

        _LOGGER.info("Converting %s to %s", input_path, output_path)

        # Build the Supervisor API URL and payload
        addon_slug = "addon_svg_to_png"  # your add-on slug
        # The Supervisor API endpoint for executing a command in an add-on:
        url = f"http://supervisor/api/hassio/addons/{addon_slug}/exec"
        
        # Retrieve the Supervisor token (this should be available on a supervised system)
        token = os.environ.get("HASSIO_TOKEN")
        if not token:
            raise RuntimeError("HASSIO_TOKEN not found; ensure Supervisor API access is enabled.")

        headers = {"X-Hassio-Token": token}
        payload = {
            "command": ["python3", "/convert.py", input_path, output_path]
        }

        try:
            # Note: Depending on your use case, you might need to adjust timeout and error handling.
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            _LOGGER.info("Conversion successful, response: %s", response.json())
        except requests.exceptions.RequestException as err:
            raise RuntimeError(f"Conversion failed: {err}")

    # Register the service
    hass.services.register("svg_to_png", "convert", handle_convert, schema=SERVICE_SCHEMA)
    
    return True

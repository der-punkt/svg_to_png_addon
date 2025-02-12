import logging
import subprocess
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

        _LOGGER.info(f"Converting {input_path} to {output_path}")

        # Call the add-on
        try:
            subprocess.run(
                ["docker", "exec", "addon_svg_to_png", "python3", "/convert.py", input_path, output_path],
                check=True
            )
            _LOGGER.info("Conversion successful")
        except subprocess.CalledProcessError as e:
            _LOGGER.error(f"Conversion failed: {e}")

    # Register the service
    hass.services.register("svg_to_png", "convert", handle_convert, schema=SERVICE_SCHEMA)
    
    return True

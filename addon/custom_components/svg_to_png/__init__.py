import os
import logging

import requests
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "svg_to_png"

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    port = config[DOMAIN].get("port", 5000)  # Read port from configuration with default 5000
    addon_slug = config[DOMAIN].get("addon_slug", "f38d7a98-svg-to-png").replace("_", "-")  # Read addon slug from configuration with default and replace underscores with hyphens
    api_endpoint = config[DOMAIN].get("api_endpoint", "/convert")  # Read API endpoint from configuration with default

    def handle_convert_svg_to_png(call: ServiceCall) -> None:
        svg_path = call.data.get("input_path")
        png_path = call.data.get("output_path")

        if not svg_path or not png_path:
            _LOGGER.error("SVG path and PNG path must be provided")
            return

        if not os.path.isfile(svg_path):
            _LOGGER.error("SVG file does not exist: %s", svg_path)
            return

        try:
            # Call the svg_to_png addon (assuming it's a function)
            png_content = svg_to_png(svg_path, port, addon_slug, api_endpoint)

            with open(png_path, "wb") as png_file:
                png_file.write(png_content)

            _LOGGER.info("Successfully converted SVG to PNG: %s", png_path)
        except Exception as e:
            _LOGGER.error("Error converting SVG to PNG: %s", e)

    hass.services.register(DOMAIN, "convert", handle_convert_svg_to_png)
    return True

def svg_to_png(svg_path: str, port: int, addon_slug: str, api_endpoint: str) -> bytes:
    addon_url = f"http://{addon_slug}:{port}{api_endpoint}"  # Use add-on hostname, port, and API endpoint
    try:
        with open(svg_path, 'rb') as f:
            files = {'file': (os.path.basename(svg_path), f, 'image/svg+xml')}
            response = requests.post(addon_url, files=files, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Conversion failed: {e}")
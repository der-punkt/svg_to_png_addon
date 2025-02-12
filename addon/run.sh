#!/bin/sh
echo "🚀 SVG to PNG Add-on Started..."

# Ensure the custom_components directory exists in Home Assistant
mkdir -p /config/custom_components/svg_to_png

# Copy the custom component files only if they are missing
if [ ! -f "/config/custom_components/svg_to_png/__init__.py" ]; then
    cp -r /tmp/svg_to_png/* /config/custom_components/svg_to_png/
    echo "✅ Copied svg_to_png integration to /config/custom_components/"
else
    echo "⚠️ svg_to_png integration already exists. Skipping copy."
fi


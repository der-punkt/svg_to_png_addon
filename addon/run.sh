#!/bin/sh

echo "🚀 SVG to PNG Add-on Started..."

# Wait for /config/ to be available (just in case)
sleep 2

# Ensure we can write to /config/
if [ ! -w /config ]; then
    echo "❌ Error: /config/ is read-only. Cannot copy files."
    exit 1
fi

# Ensure the custom_components directory exists in Home Assistant
mkdir -p /config/custom_components/svg_to_png

# Copy the custom component files only if they are missing
if [ ! -f "/config/custom_components/svg_to_png/__init__.py" ]; then
    cp -r /tmp/svg_to_png/* /config/custom_components/svg_to_png/
    chmod -R 644 /config/custom_components/svg_to_png  # ✅ Fix permissions at runtime
    echo "✅ Copied svg_to_png integration to /config/custom_components/ and fixed permissions"
else
    echo "⚠️ svg_to_png integration already exists. Skipping copy."
fi

exec tail -f /dev/null

#!/bin/sh

echo "🚀 SVG to PNG Add-on Started..."

# Wait for /config/ to be available (just in case)
sleep 2

# Ensure we can write to /config/
if [ ! -w /config ]; then
    echo "❌ Error: /config/ is read-only. Cannot copy files."
    exit 1
else
    echo "✍️ /config/ can be written."
fi

# Ensure the custom_components directory exists
if mkdir -p /config/custom_components/svg_to_png; then
    echo "✅ Created directory /config/custom_components/svg_to_png"
else
    echo "❌ Failed to create directory /config/custom_components/svg_to_png"
    exit 1
fi

# Copy the custom component files only if they are missing
if [ ! -f "/config/custom_components/svg_to_png/__init__.py" ]; then
    if cp -r /tmp/svg_to_png/* /config/custom_components/svg_to_png/; then
        echo "✅ Copied svg_to_png integration to /config/custom_components/"
    else
        echo "❌ Failed to copy files to /config/custom_components/"
        exit 1
    fi

    if chmod -R 644 /config/custom_components/svg_to_png; then
        echo "✅ Set correct permissions on /config/custom_components/svg_to_png"
    else
        echo "❌ Failed to set permissions on /config/custom_components/svg_to_png"
        exit 1
    fi
else
    echo "⚠️ svg_to_png integration already exists. Skipping copy."
fi

exec tail -f /dev/null

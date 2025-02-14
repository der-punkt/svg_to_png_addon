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

SLUG="svg_to_png"
CUSTOM_COMPONENT_PATH="/config/custom_components/$SLUG"
VERSION_FILE="$CUSTOM_COMPONENT_PATH/.version"
ADDON_VERSION="1.4.9"  # Change this when updating the add-on
CONFIG_PATH=/data/options.json

# Ensure the custom_components directory exists
if mkdir -p "$CUSTOM_COMPONENT_PATH"; then
    echo "✅ Created directory $CUSTOM_COMPONENT_PATH"
else
    echo "❌ Failed to create directory $CUSTOM_COMPONENT_PATH"
    exit 1
fi

# Check if version exists and matches
if [ -f "$VERSION_FILE" ] && [ "$(cat $VERSION_FILE)" = "$ADDON_VERSION" ]; then
    echo "⚠️ $SLUG integration is up-to-date (version $ADDON_VERSION). Skipping copy."
else
    echo "🔄 Updating $SLUG integration to version $ADDON_VERSION..."

    # Copy the custom component files
    if cp -r /tmp/$SLUG/* "$CUSTOM_COMPONENT_PATH/"; then
        echo "✅ Copied $SLUG integration to $CUSTOM_COMPONENT_PATH"
    else
        echo "❌ Failed to copy files to $CUSTOM_COMPONENT_PATH"
        exit 1
    fi

    # Set correct permissions
    if chmod -R 644 "$CUSTOM_COMPONENT_PATH"; then
        echo "✅ Set correct permissions on $CUSTOM_COMPONENT_PATH"
    else
        echo "❌ Failed to set permissions on $CUSTOM_COMPONENT_PATH"
        exit 1
    fi

    # Save the current version
    echo "$ADDON_VERSION" > "$VERSION_FILE"
    echo "✅ Version updated to $ADDON_VERSION"

    # Reminder to restart Home Assistant
    echo "🔄 Please restart Home Assistant for the changes to take effect!"
fi

echo "🌐 Starting the Flask app..."
exec python3 convert.py

ARG BUILD_FROM=ghcr.io/hassio-addons/base:17.1.3
FROM $BUILD_FROM

# Install Python, CairoSVG, and dependencies using APK
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-cairosvg \
    cairo \
    pango \
    gdk-pixbuf \
    musl-dev \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev

# # Copy the Home Assistant custom component
# COPY custom_components/svg_to_png /config/custom_components/svg_to_png
# RUN chmod -R 755 /config/custom_components/svg_to_png

# Copy the conversion script
COPY convert.py /convert.py
RUN chmod +x /convert.py

# Copy starting script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
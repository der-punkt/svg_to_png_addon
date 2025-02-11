ARG BUILD_FROM=ghcr.io/hassio-addons/base:latest
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    cairo \
    cairo-dev \
    pango \
    pango-dev \
    gdk-pixbuf \
    gdk-pixbuf-dev \
    py3-pip

# Install Python libraries
RUN pip install cairosvg

# Copy the script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]

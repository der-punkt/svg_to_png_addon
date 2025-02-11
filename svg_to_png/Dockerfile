ARG BUILD_FROM=ghcr.io/hassio-addons/base:latest
FROM $BUILD_FROM

# Install required system dependencies
RUN apk add --no-cache \
    cairo \
    cairo-dev \
    pango \
    pango-dev \
    gdk-pixbuf \
    gdk-pixbuf-dev \
    py3-pip \
    python3-dev \
    musl-dev \
    gcc \
    libc-dev \
    libffi-dev

# Upgrade pip and install CairoSVG
RUN pip install --upgrade pip && pip install cairosvg

# Copy the conversion script
COPY convert.py /convert.py

# Make script executable
RUN chmod +x /convert.py

CMD ["tail", "-f", "/dev/null"]

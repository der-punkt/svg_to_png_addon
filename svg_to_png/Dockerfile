ARG BUILD_FROM=ghcr.io/hassio-addons/base:17.1.3
FROM $BUILD_FROM

# Install Python and pip
RUN apk add --no-cache \
    python3 \
    py3-pip \
    cairo \
    pango \
    gdk-pixbuf \
    musl-dev \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev

# Upgrade pip and install CairoSVG
RUN python3 -m ensurepip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir cairosvg

# Copy script
COPY convert.py /convert.py
RUN chmod +x /convert.py

CMD ["python3", "/convert.py"]

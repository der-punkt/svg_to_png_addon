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

# Copy script
COPY convert.py /convert.py
RUN chmod +x /convert.py

CMD ["python3", "/convert.py"]

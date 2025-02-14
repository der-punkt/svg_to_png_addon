ARG BUILD_FROM=ghcr.io/hassio-addons/base:17.1.3
FROM $BUILD_FROM

# Install Python, CairoSVG, and dependencies using APK
RUN apk add --no-cache \
#    python3 \
#    py3-pip \
    py3-cairosvg \
#    cairo \
#    pango \
#    gdk-pixbuf \
#    musl-dev \
#    gcc \
#    libc-dev \
#    libffi-dev \
    py3-flask 
    
# Copy the conversion script
COPY convert.py /convert.py
RUN chmod +x /convert.py

# Copy starting script
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Copy the custom component at runtime instead of during build
COPY custom_components/svg_to_png /tmp/svg_to_png

EXPOSE 5000

CMD [ "/run.sh" ]
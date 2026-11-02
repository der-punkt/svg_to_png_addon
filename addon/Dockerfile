ARG BUILD_FROM=ghcr.io/hassio-addons/base:17.1.3
FROM $BUILD_FROM

# Install Python, CairoSVG, Flask, and fonts for proper SVG text rendering
RUN apk add --no-cache \
    py3-cairosvg \
    py3-flask \
    fontconfig \
    font-roboto \
    font-dejavu

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
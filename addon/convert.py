"""
This script provides functionality to convert SVG files to PNG format using the CairoSVG library.
It includes a Flask web server to handle file upload requests for conversion and a command-line
interface for converting files directly.
Modules:
    sys: Provides access to some variables used or maintained by the interpreter.
    cairosvg: A library to convert SVG files to PNG format.
    os: Provides a way of using operating system dependent functionality.
    logging: Provides a way to configure and use loggers.
    flask: A micro web framework for Python.
Functions:
    convert_file_obj(file_obj):
    convert_file_obj_route():
    convert_path(svg_path, png_path):
Usage:
    Run the script with the "convert" argument followed by the input SVG file path and output PNG file path
    to convert a file directly:
        python convert.py convert <input_svg> <output_png>
    Alternatively, run the script without arguments to start the Flask web server:
        python convert.py
"""

import sys
import cairosvg
import os
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Default port (can be overridden by environment variable)
DEFAULT_PORT = 5000

def convert_file_obj(file_obj):
    """
    Convert an SVG file object to PNG format.
    This function converts the SVG data contained in the provided file-like object into
    PNG image data using CairoSVG's svg2png function. It logs a success message if the conversion
    is successful, or logs an error and re-raises the exception if any error occurs.
    Parameters:
        file_obj: A file-like object containing SVG data.
    Returns:
        The PNG image data as bytes.
    Raises:
        Exception: Propagates any exception raised during the SVG to PNG conversion process.
    """

    try:
        png_data = cairosvg.svg2png(file_obj=file_obj)
        logger.info("Conversion successful")
        return png_data
    except Exception as e:
        logger.error(f"Error converting file: {e}")
        raise e

@app.route('/convert', methods=['POST'])
def convert_file_obj_route():
    """
    Handle the file upload route for converting SVG/SVGZ files to PNG.
    This function processes a file upload request, checks if the uploaded file is an SVG or SVGZ file,
    and converts it to PNG format. It returns the PNG data with appropriate HTTP status codes and 
    content type headers.
    Returns:
        tuple: A tuple containing the response data, HTTP status code, and headers.
    Possible Responses:
        - 200: PNG data with 'Content-Type' header set to 'image/png'.
        - 400: JSON response with an error message if the file part is missing, no file is selected, 
               or the file type is invalid.
        - 500: JSON response with an error message if there is an error during the conversion process 
               or any other exception occurs.
    """
    try:
        if 'file' not in request.files:
            logger.error('No file part')
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            logger.error('No selected file')
            return jsonify({'error': 'No selected file'}), 400

        if file and file.filename.lower().endswith(('.svg', '.svgz')):
            
            try:
                png_data = convert_file_obj(file)
                return png_data, 200, {'Content-Type': 'image/png'}
            except Exception as e:
                return jsonify({'error': f'SVG to PNG conversion failed: {e}'}), 500

        else:
            logger.error('Invalid file type. Only SVG or SVGZ allowed')
            return jsonify({'error': 'Invalid file type. Only SVG or SVGZ allowed'}), 400

    except Exception as e:
        logger.error(f'Error converting file: {e}')
        return jsonify({'error': f'Error converting file: {e}'}), 500

def convert_path(svg_path, png_path):
    """
    Converts an SVG file to a PNG file by reading the SVG file from the provided svg_path,
    processing it with convert_file_obj, and writing the resulting PNG data to png_path.
    Parameters:
        svg_path (str): The file path to the source SVG file.
        png_path (str): The file path where the output PNG file will be saved.
    Raises:
        Exception: Any exception encountered during file operations or the conversion process
                   is logged and re-raised.
    """
    
    try:
        with open(svg_path, 'rb') as svg_file:
            png_data = convert_file_obj(svg_file)
                
            with open(png_path, 'wb') as png_file:
                png_file.write(png_data)
                logger.info(f"Conversion successful, saved to {png_path}")

    except Exception as e:
        logger.error(f"Failed to convert {svg_path} to {png_path}: {e}")
        raise e

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "convert": # Check if run as a script
        if len(sys.argv) != 4:
            logger.error("Usage: convert.py convert <input_svg> <output_png>")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]

        convert_path(input_file, output_file)
    
    else: # Run as Flask server
        debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
        port = int(os.environ.get("FLASK_PORT", DEFAULT_PORT))
        app.run(debug=debug_mode, host='0.0.0.0', port=port)  # Use the configured port
        logger.info(f"Flask server started on port {port}") # Log the port for verification

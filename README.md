# Home Assistant Add-on: SVG to PNG Converter

## Overview
This Home Assistant add-on provides a simple way to convert SVG images to PNG format using an integrated conversion service. The add-on runs a lightweight service inside a Docker container and exposes a custom service for easy integration with Home Assistant.

## Features
- Converts SVG images to PNG format.
- Integrates seamlessly with Home Assistant services.
- Uses **CairoSVG** for accurate and high-quality rendering.
- Works on multiple architectures (amd64, armv7, aarch64).

## Installation
### **Step 1: Add the Repository**
1. Open **Home Assistant**.
2. Navigate to **Settings** > **Add-ons** > **Add-on Store**.
3. Click the **three dots** in the top-right corner and select **Repositories**.
4. Add the following URL:
   ```
   https://github.com/your-username/svg_to_png_addon
   ```
5. Click **Add** and wait for the repository to load.

### **Step 2: Install the Add-on**
1. Locate **SVG to PNG Converter** in the add-on store.
2. Click **Install**.
3. Once installed, configure the options as needed.
4. Start the add-on with privileged access (required).

## Usage
### **Calling the Service in Home Assistant**
Once installed, you can use the custom **service** to convert an SVG file.

#### **Service Name:**
```
svg_to_png.convert
```

#### **Service Data Example:**
```yaml
service: svg_to_png.convert
data:
  input_file: "/media/tmp/image.svg"
  output_file: "/media/tmp/image.png"
```

### **How It Works**
1. The Home Assistant service sends a request to the add-on.
2. The add-on runs `cairosvg` inside the Docker container to convert the file.
3. The PNG file is saved in the specified location.

## Logs & Debugging
To check the add-on logs:
```bash
ha addons logs svg_to_png
```
If you encounter issues, make sure:
- The file paths are correct.
- The add-on has sufficient permissions.
- Docker is running properly.

## Contributing
Feel free to contribute by submitting **pull requests** or opening **issues** on GitHub!

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
⭐ **Enjoy using the SVG to PNG Converter?** Consider starring the repository on GitHub! ⭐


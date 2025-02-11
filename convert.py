import sys
import cairosvg

def convert_svg_to_png(input_path, output_path):
    try:
        cairosvg.svg2png(url=input_path, write_to=output_path)
        print(f"Conversion successful: {output_path}")
    except Exception as e:
        print(f"Error converting file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert.py <input_svg> <output_png>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_svg_to_png(input_file, output_file)

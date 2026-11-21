
from PIL import Image
import sys

# Usage: python3 image_to_kic.py input.png output.kic

if len(sys.argv) != 3:
    print("Usage: python3 image_to_kic.py input.png output.kic")
    raise SystemExit(1)

source, destination = sys.argv[1], sys.argv[2]

# Resize to the Kiwi OS icon dimensions.
image = Image.open(source).convert("RGBA")
image = image.resize((16, 16), Image.Resampling.LANCZOS)

pixels = []

for r, g, b, a in image.getdata():
    # Transparent pixels become the desktop's green color.
    if a < 128:
        pixels.append(2)
        continue

    # Pick a simple VGA color based on the pixel's RGB values.
    if r < 48 and g < 48 and b < 48:
        color = 0       # Black
    elif r > 200 and g > 200 and b > 200:
        color = 15      # White
    elif r > 180 and g > 140 and b < 100:
        color = 14      # Yellow
    elif r > g * 1.4 and r > b * 1.4:
        color = 4       # Red
    elif g > r * 1.2 and g > b * 1.2:
        color = 10      # Bright green
    elif b > r * 1.2 and b > g * 1.1:
        color = 9       # Bright blue
    else:
        color = 7       # Light gray

    pixels.append(color)

with open(destination, "wb") as file:
    file.write(bytes(pixels))

print(f"Created {destination}: {len(pixels)} pixels, {len(pixels)} bytes")


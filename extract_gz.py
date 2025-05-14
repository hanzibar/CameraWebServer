import re
import sys

# Path to the C header file
HEADER_FILE = "camera_index.h"

# Read the header file and extract all C arrays
with open(HEADER_FILE, "r") as f:
    content = f.read()

# Find all matching arrays
# Pattern: const unsigned char <name>[] = { ... };
pattern = re.compile(r'const unsigned char (\w+)_html_gz\[\] = \{(.+?)\};', re.DOTALL)
matches = pattern.findall(content)

if not matches:
    print("Could not find any gzipped data arrays in header file.")
    sys.exit(1)

for name, array_body in matches:
    # Extract the hex byte values
    hex_bytes = re.findall(r'0x[0-9A-Fa-f]{2}', array_body)
    byte_data = bytes([int(b, 16) for b in hex_bytes])
    # Determine output filename
    base_name = name.replace('_html_gz', '')
    output_gz = f"{base_name}.html.gz"
    with open(output_gz, "wb") as out_f:
        out_f.write(byte_data)
    print(f"Extracted {len(byte_data)} bytes to {output_gz}")

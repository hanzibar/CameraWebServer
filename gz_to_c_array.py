import sys
import os

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <gz_file> <array_name> <header_file>")
    sys.exit(1)

GZ_FILE = sys.argv[1]
ARRAY_NAME = sys.argv[2]
HEADER_FILE = sys.argv[3]

with open(GZ_FILE, "rb") as f:
    data = f.read()

mode = "a" if os.path.exists(HEADER_FILE) and os.path.getsize(HEADER_FILE) > 0 else "w"
with open(HEADER_FILE, mode) as f:
    f.write(f"//File: {os.path.basename(GZ_FILE)}, Size: {len(data)}\n")
    f.write(f"#define {ARRAY_NAME}_len {len(data)}\n")
    f.write(f"const unsigned char {ARRAY_NAME}[] = {{\n  ")
    for i, byte in enumerate(data):
        if i > 0:
            if i % 20 == 0:
                f.write("\n  ")
            else:
                f.write(" ")
        f.write(f"0x{byte:02X},")
    f.write("\n};\n\n")

print(f"Converted {GZ_FILE} to {HEADER_FILE} as C array.")

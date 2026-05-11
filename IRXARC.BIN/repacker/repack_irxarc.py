import os
import json
import zlib
import struct
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("output_file")
Gargs = parser.parse_args()

HDR="""
 _____________   __  ___  ______  _____    ______ ___________  ___  _____  _   __ ___________ 
|_   _| ___ \\ \\ / / / _ \\ | ___ \\/  __ \\   | ___ \\  ___| ___ \\/ _ \\/  __ \\| | / /|  ___| ___ \\
  | | | |_/ /\\ V / / /_\\ \\| |_/ /| /  \\/   | |_/ / |__ | |_/ / /_\\ \\ /  \\/| |/ / | |__ | |_/ /
  | | |    / /   \\ |  _  ||    / | |       |    /|  __||  __/|  _  | |    |    \\ |  __||    /
 _| |_| |\\ \\/ /^\\ \\| | | || |\\ \\ | \\__/\\   | |\\ \\| |___| |   | | | | \\__/\\| |\\  \\| |___| |\\ \\
 \\___/\\_| \\_\\/   \\/\\_| |_/\\_| \\_| \\____/   \\_| \\_\\____/\\_|   \\_| |_/\\____/\\_| \\_/\\____/\\_| \\_|
"""
print(HDR)

ENTRY_HEADER_SIZE = 0x140


def scramble(data):
    out = bytearray(len(data))

    for i, b in enumerate(data):
        out[i] = b ^ (~(i & 0xA5) & 0xFF)

    return bytes(out)


def align16(x):
    return (x + 0xF) & ~0xF


def write_cstring(buf, offset, max_len, text):
    encoded = text.encode("ascii")

    encoded = encoded[:max_len - 1]

    buf[offset:offset + len(encoded)] = encoded
    buf[offset + len(encoded)] = 0

print("-- Opening manifest file from source folder")
with open(f"{Gargs.input_dir}/_manifest.json", "r") as f:
    manifest = json.load(f)

entries = manifest["entries"]
out = bytearray()

#
# global header
#
global_hdr = bytearray(0x40)
global_hdr[0] = len(entries)
print(f"-- {global_hdr[0]} entries will be packed")

out += global_hdr

for index, entry in enumerate(entries):

    filepath = f"{Gargs.input_dir}/{entry['filename']}"

    with open(filepath, "rb") as f:
        elf_data = f.read()

    elf_size = len(elf_data)

    padded_size = align16(elf_size)
    header = bytearray(ENTRY_HEADER_SIZE)
    struct.pack_into("<I", header, 0x00, padded_size)
    args = entry.get("args", "").encode("latin1")

    if args:
        struct.pack_into("<I", header, 0x04, len(args))

    write_cstring(header, 0x10, 0x30, entry["filename"])
    header[0x40:0x40 + len(args)] = args #write_cstring(header, 0x40, 0x30, args)

    out += header
    out += elf_data

    #
    # padding
    #
    while len(out) % 16:
        out.append(0)

    print(f"[ADD]: {entry['filename']:<48} size=0x{padded_size:08X} args={args}")

compressed = zlib.compress(bytes(out), level=9)

final = scramble(compressed)

with open(Gargs.output_file, "wb") as f:
    f.write(final)

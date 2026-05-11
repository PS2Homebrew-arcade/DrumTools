import zlib
import json
import argparse
import struct
import os

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output_unscrambled")
parser.add_argument("output_unpacked")
args = parser.parse_args()

HDR = """
 _____________   __  ___  ______  _____   _   _ _   _ ______  ___  _____  _   __ ___________ 
|_   _| ___ \\ \\ / / / _ \\ | ___ \\/  __ \\ | | | | \\ | || ___ \\/ _ \\/  __ \\| | / /|  ___| ___ \\
  | | | |_/ /\\ V / / /_\\ \\| |_/ /| /  \\/ | | | |  \\| || |_/ / /_\\ \\ /  \\/| |/ / | |__ | |_/ /
  | | |    / /   \\ |  _  ||    / | |     | | | | . ` ||  __/|  _  | |    |    \\ |  __||    / 
 _| |_| |\\ \\/ /^\\ \\| | | || |\\ \\ | \\__/\\ | |_| | |\\  || |   | | | | \\__/\\| |\\  \\| |___| |\\ \\ 
 \\___/\\_| \\_\\/   \\/\\_| |_/\\_| \\_| \\____/  \\___/\\_| \\_/\\_|   \\_| |_/\\____/\\_| \\_/\\____/\\_| \\_|

"""

print(HDR)


ENTRY_HEADER_SIZE = 0x140

def read_cstring(buf, offset, max_len):
    end = offset

    while end < offset + max_len and buf[end] != 0:
        end += 1

    return buf[offset:end].decode("ascii", errors="ignore")

def align16(x):
    return (x + 0xF) & ~0xF

# 0x140 bytes of header
# my assumption
# uint64_t irx_size;
# uint64_t arg_size;
# char filename[0x30];
# char args[0x30]; <- ASSUMPTION
# unsigned char unused[0xDC];
#
def dump_irxarc(data):
    outdir=f"unc_{args.input}"
    entry_count = data[0]
    manifest = {
        "entry_count": entry_count,
        "original_filename":args.input,
        "entries": []
    }

    print(f"-- Ammount of files inside: {entry_count}")
    print()
    os.makedirs(outdir, exist_ok=True)

    current = 0

    for index in range(entry_count):

        # first entry has global 0x40-byte prefix
        if index == 0:
            current += 0x40

        header_start = current

        # guessed structure
        irx_size = struct.unpack_from("<I", data, current + 0x00)[0]
        arg_size = struct.unpack_from("<I", data, current + 0x04)[0]

        filename = read_cstring(data, current + 0x10, 0x30)
        irxargs     = read_cstring(data, current + 0x40, 0x30)

        elf_offset = current + ENTRY_HEADER_SIZE

        out_name = filename if filename else f"unnamed_{index:02d}.irx"
        elf_data = data[elf_offset:elf_offset + irx_size]
        with open(f"{outdir}/{out_name}", "wb") as f:
            f.write(elf_data)

        manifest["entries"].append({
            "filename": out_name,
            "args": irxargs,
            "arg_size": arg_size,
            "header_offset": header_start,
            "elf_offset": elf_offset,
            "original_size": irx_size
        })

        print(f"[{index:02d}]")
        print(f"  Filename      : {filename}")
        print(f"  Size          : 0x{irx_size:X} ({irx_size})")
        print(f"  Arg Size      : 0x{arg_size:X} ({arg_size})")
        if irxargs:
            print(f"  Args          : {irxargs}")
        print(f"  Header Offset : 0x{header_start:08X}")
        print(f"  ELF Offset    : 0x{elf_offset:08X}")


        # sanity check
        elf_magic = data[elf_offset:elf_offset + 4]

        if elf_magic != b"\x7FELF":
            print(f"  INVALID ELF MAGIC")

        print()

        # next entry
        current = align16(elf_offset + irx_size)
    

    with open(f"{outdir}/_manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    print(f"decompression finished, all the extracted files available inside folder '{outdir}/_manifest.json'")
    print("file '_manifest.json' holds metadata from the original file")

def unscrambl(data):
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ (~(i & 0xA5) & 0xFF)
    return bytes(out)

print("-- Opening 'IRXARC.BIN'")

with open(args.input, "rb") as f:
    data = f.read()

print("-- unscrambling data")
data = unscrambl(data)
    
if args.output_unscrambled != "-":
    with open(args.output_unscrambled, "wb") as f:
        f.write(data)

out = zlib.decompress(data)

with open(args.output_unpacked, "wb") as f:
    f.write(out)

dump_irxarc(out)

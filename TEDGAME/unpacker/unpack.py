import argparse


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

HDR = """
 _____ ___________ _____   ___  ___  ___ _____   _   _ _   _ ______  ___  _____  _   __ ___________ 
|_   _|  ___|  _  \\  __ \\ / _ \\ |  \\/  ||  ___| | | | | \\ | || ___ \\/ _ \\/  __ \\| | / /|  ___| ___ \\
  | | | |__ | | | | |  \\// /_\\ \\| .  . || |__   | | | |  \\| || |_/ / /_\\ \\ /  \\/| |/ / | |__ | |_/ /
  | | |  __|| | | | | __ |  _  || |\\/| ||  __|  | | | | . ` ||  __/|  _  | |    |    \\ |  __||    / 
  | | | |___| |/ /| |_\\ \\| | | || |  | || |___  | |_| | |\\  || |   | | | | \\__/\\| |\\  \\| |___| |\\ \\ 
  \\_/ \\____/|___/  \\____/\\_| |_/\\_|  |_/\\____/   \\___/\\_| \\_/\\_|   \\_| |_/\\____/\\_| \\_/\\____/\\_| \\_|
"""

print(HDR)

def decompr(data):
    src = 4
    dst = bytearray()

    bVar1 = data[src]
    src += 1

    while bVar1 != 0:
        uVar3 = bVar1

        if uVar3 < 2:
            bVar1 = data[src]
        else:
            while True:
                bit = uVar3 & 1
                uVar3 >>= 1

                if bit == 0:
                    word = (data[src] << 8) | data[src+1]
                    src += 2

                    offset = word & 0x7FF
                    if offset == 0:
                        offset = 0x800

                    length = (word >> 11) & 0x1F
                    if length == 0:
                        length = 0x20

                    for _ in range(length):
                        dst.append(dst[-offset])

                else:
                    dst.append(data[src])
                    src += 1

                if uVar3 <= 1:
                    break

            bVar1 = data[src]

        src += 1

    return bytes(dst)



print("-- Opening", args.input)


with open(args.input, "rb") as f:
    data = f.read()

print("-- input file size:", len(data))

stream = bytes(data)
out = decompr(stream)
print("-- decompression output size:", len(out))

with open(args.output, "wb") as f:
    written = f.write(out)
    print("-- written", written, "bytes into output file")
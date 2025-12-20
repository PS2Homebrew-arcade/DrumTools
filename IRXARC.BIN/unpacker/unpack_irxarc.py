import zlib

HDR = """
 _____________   __  ___  ______  _____   _   _ _   _ ______  ___  _____  _   __ ___________ 
|_   _| ___ \\ \\ / / / _ \\ | ___ \\/  __ \\ | | | | \\ | || ___ \\/ _ \\/  __ \\| | / /|  ___| ___ \\
  | | | |_/ /\\ V / / /_\\ \\| |_/ /| /  \\/ | | | |  \\| || |_/ / /_\\ \\ /  \\/| |/ / | |__ | |_/ /
  | | |    / /   \\ |  _  ||    / | |     | | | | . ` ||  __/|  _  | |    |    \\ |  __||    / 
 _| |_| |\\ \\/ /^\\ \\| | | || |\\ \\ | \\__/\\ | |_| | |\\  || |   | | | | \\__/\\| |\\  \\| |___| |\\ \\ 
 \\___/\\_| \\_\\/   \\/\\_| |_/\\_| \\_| \\____/  \\___/\\_| \\_/\\_|   \\_| |_/\\____/\\_| \\_/\\____/\\_| \\_|

"""

print(HDR)

def unscrambl(data):
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ (~(i & 0xA5) & 0xFF)
    return bytes(out)

print("-- Opening 'IRXARC.BIN'")

with open("IRXARC.BIN", "rb") as f:
    data = f.read()

print("-- unscrambling data")
data = unscrambl(data)
    
with open("IRXARC.UNSCRAMBLED", "wb") as f:
    f.write(data)

out = zlib.decompress(data)

with open("IRXARC.UNPACKED", "wb") as f:
    f.write(out)

print("-- DONE: outpout len ", len(out))
# Unpacker for `IRXARC.BIN`

thanks to namco for leaving the following string on the binary, saving investigation time
```
deflate 1.2.1 Copyright 1995-2003 Jean-loup
```

## usage
```
python unpack_irxarc.py INPUT UNSCRAMBLED UNPACKED
```
- `INPUT`: the location of the `IRXARC.BIN` file to process
- `UNSCRAMBLED`: binary zlib file after being un-scrambled. not useful really, pass `-` here to avoid it's creation
- `UNPACKED`: decompressed IRXARC file

also, after unpacking, the contents of the IRXARC will be displayed, and a new folder called like the input file, but with `unc_` prefix, will be created
holding the extracted files as well as all the necesary metadata from the archive un a JSON file `_manifest.json`

## data and layout

the file is scrambled and compressed.

preliminar structure

main header
```c
typedef struct { // size: 0x40
  uint8_t itemcount; // size needs confirmation
  uint8_t unknown[0x3F];
}main_header_t;

typedef struct { // size: 0x140
  uint64_t irx_size;
  uint64_t irx_args;
  char filename[0x30];
  char irx_args[0x30]; // cant know for sure, everything else is zeroed
  char fill[0xD8];
}entry_t;
```

the general layour of the file is
```
MAIN_HEADER
  ENTRY
   DATA
  ENTRY1
   DATA1
  ENTRY2
   DATA2
  ENTRY...N
   DATA...N
```

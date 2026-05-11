# Repacker for `IRXARC.BIN`

this script is capable of rebuilding IRXARC.BIN files for the Taiko no tatsujin games

the main purpose is to extract with the unpacker script this file, perform the desired modifications and reinject the file to the security dongle. for whatever reason we want to

to test this, the IRXARC.BIN from taiko no tatsujin 9 was unpacked and repacked as is with these scripts, yielding the **same checksum** after repacking!

## usage
```
python repack_irxarc.py INPUT_DIR OUTPUT
```

- `INPUT_DIR`: folder holding the `_manifest.json` and all the files to be repacked. pass the folder name as is, **no leading slashes**
- `OUTPUT`: compressed and scrambled `IRXARC.BIN` ready to be used for whatever purpose
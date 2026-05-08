# Region change

Namco system256 units store a regional signature on the playstation2 eeprom, exactly on the same area than retail ps2 use for storing iLink ID

TAIKO Drum games will check this signature via the ACRTC driver, wich interally calls CDVDMAN `sceCdRI()`

the driver provided here is a custom version of the open source ACRTC driver, which has been updated to feed the game with user defined data
## installation process:
1. take the ACRTC.irx file from the repository and use it to replace the `ACRTC` file from the game dongle (mind the lack of file extension on the file inside the dongle)
2. select the desired region file vector (one of the `ACREGION_*`) files, and put it inside dongle named as `ACREGION`

> if no `ACREGION` file is provided, the ASIA5 is the default value

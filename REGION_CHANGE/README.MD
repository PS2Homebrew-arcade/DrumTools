# Region change

Namco system256 units store a regional signature on the playstation2 eeprom, exactly on the same area than retail ps2 use for storing iLink ID

TAIKO Drum games will check this signature via the ACRTC driver, wich interally calls CDVDMAN `sceCdRI()`

the drivers provided here are designed to be injected into the IOPRP image inside the security dongle, when running, it will override the implementation of CDVDMAN `sceCdRI()` to return a user defined signature

## installation process:

due to copyright issues, we cannot provide you a ready to use package

What you will need to do is:

1. modify the `IOPBTCONF` file (See [IOPBTCONF](./IOPBTCONF))
2. inject the `FAKEREGION` module into the dongle `IOPRP.IMG` file
3. add the modified `IOPRP.IMG` file to the dongle
4. select the desired region file vector (one of the `ACREGION_*`) files, and put it inside dongle named `ACREGION`

the defaul signature of the driver is ASIA5

## IOPBTCONF

the original `IOPBTCONF` file looks like this:

```
!include IOPBTCONF
SIO2MAN
MCMAN
DAEMON
EESYNC2


```

you should modify it, adding the `FAKEREGION` module listed before `EESYNC2`

like this

```
!include IOPBTCONF
SIO2MAN
MCMAN
DAEMON
FAKEREGION
EESYNC2


```

## IOPRP image

to modify the IOPRP image, use [romman](https://github.com/israpps/romman) or [romimg](https://github.com/israpps/romimg)

# _____     ___ ____     ___ ____
#  ____|   |    ____|   |        | |____|
# |     ___|   |____ ___|    ____| |    \    PS2DEV Open Source Project.
#-----------------------------------------------------------------------
# Copyright ps2dev - http://www.ps2dev.org
# Licenced under Academic Free License version 2.0
# Review ps2sdk README & LICENSE files for further details.

IOP_SRC_DIR ?= src/
IOP_INC_DIR ?= $(IOP_SRC_DIR)

BASENAME = ACRTC
IOP_BIN = ../$(BASENAME).irx
IOP_OBJS = iopmain.o imports.o

all: $(IOP_BIN)

ifneq ($(DEBUG), 0)
	rm -f ../$(BASENAME).notiopmod.elf ../$(BASENAME).notiopmod.stripped.elf
endif

clean:
	rm -f -r $(IOP_OBJS) $(IOP_BIN)

ifeq ($(DEBUG), 1)
  IOP_CFLAGS += -DDEBUG=$(DEBUG)
endif

include $(PS2SDK)/Defs.make
include $(PS2SDK)/samples/Makefile.pref
include $(PS2SDK)/samples/Makefile.iopglobal
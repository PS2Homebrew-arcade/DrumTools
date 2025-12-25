# patch the responses for the NVRAM ILINK ID
IOP_SRC_DIR ?= ./
IOP_INC_DIR ?= ./

BASENAME = FAKEREGION
IOP_BIN = ../$(BASENAME).irx
IOP_OBJS = main.o ioplib.o imports.o
IOP_CFLAGS += -DRETVAL=$(RETVAL)

all: $(IOP_BIN)
	cp $(IOP_BIN) FAKEREGION

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

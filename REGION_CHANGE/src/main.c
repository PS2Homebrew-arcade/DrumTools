#include "irx_imports.h"
#include "ioplib.h"
#include <tamtypes.h>
#include <stdint.h>

#define MODNAME "S256Region"
#define MAJOR 1
#define MINOR 0
IRX_ID(MODNAME, MAJOR, MINOR);

iop_library_t *CDVDMAN = NULL;

#define SYSTEM256_NVM_ASIA4_IDENTIFIER 0x32, 0x1F, 0xC7, 0xFA, 0xD6, 0xEE, 0xF0, 0x1C // 32 1F C7 FA D6 EE F0 1C
#define SYSTEM256_NVM_ASIA5_IDENTIFIER 0x41, 0x46, 0x53, 0x2F, 0x1E, 0xFD, 0x0F, 0xE0 // 41 46 53 2F 1E FD 0F E0
#define SYSTEM256_NVM_JAPAN_IDENTIFIER 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF

#define DEFREG SYSTEM256_NVM_ASIA5_IDENTIFIER

uint8_t ForcedRegion[8] = {DEFREG};

typedef int (*sceCdRI_t)(u8 *buffer, u32 *status);
sceCdRI_t p_sceCdRI;
int hooked_sceCdRI(u8 *buffer, u32 *status) {
    printf("!!! %s has been called\n", __FUNCTION__);
	int retval = 1;
	char rdata[9];

	*status = 0;
	memcpy(buffer, (u8*)ForcedRegion, sizeof(ForcedRegion));
	return retval;
}

int _start(int argc, char** argv) {
    printf("%s module startup\n", MODNAME);

    int fd = open("mc0:ACREGION", O_RDONLY);
    if (fd > 0) {
        printf("ACREGION: replacing regional signature\n");
        if (read(fd, (void*)ForcedRegion, sizeof(ForcedRegion)) == sizeof(ForcedRegion)) {
            printf("{%02X %02X %02X %02X %02X %02X %02X %02X}\n",
                ForcedRegion[0], ForcedRegion[1], ForcedRegion[2], ForcedRegion[3],
                ForcedRegion[4], ForcedRegion[5], ForcedRegion[6], ForcedRegion[7]
                );
        }
    }
    CDVDMAN = ioplib_getByName("cdvdman");
    if (CDVDMAN) {
        printf("hooking sceCdRI()\n");
        p_sceCdRI = ioplib_hookExportEntry(CDVDMAN, 22, hooked_sceCdRI); //ACRTC.IRX will use this to read regional signature
        printf("sceCdRI(): original:%p | new:%p\n", (void*)p_sceCdRI, (void*)hooked_sceCdRI);
        return MODULE_RESIDENT_END;
    }

    printf("failed to hook CDVDMAN\n");
    return MODULE_NO_RESIDENT_END;
}


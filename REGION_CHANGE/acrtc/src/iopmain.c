/*
# _____     ___ ____     ___ ____
#  ____|   |    ____|   |        | |____|
# |     ___|   |____ ___|    ____| |    \    PS2DEV Open Source Project.
#-----------------------------------------------------------------------
# Copyright ps2dev - http://www.ps2dev.org
# Licenced under Academic Free License version 2.0
# Review ps2sdk README & LICENSE files for further details.
*/

#include <irx_imports.h>

// Text section hash:
// a9e8a86ab5829f75b845b3e232aca4c9
// Known titles:
// NM00012
// NM00016
// NM00020
// NM00025
// Path strings: /home/ha/setrtc/iop/

typedef union acValue_stru
{
	sceCdCLOCK rtc;
	u8 id[8];
} acValue;

typedef struct acData_stru
{
	int ret;
	acValue data;
} acData;

static acData buffer;
static SifRpcDataQueue_t qd;
static SifRpcServerData_t sd;

#define SYSTEM256_NVM_ASIA4_IDENTIFIER 0x32, 0x1F, 0xC7, 0xFA, 0xD6, 0xEE, 0xF0, 0x1C // 32 1F C7 FA D6 EE F0 1C
#define SYSTEM256_NVM_ASIA5_IDENTIFIER 0x41, 0x46, 0x53, 0x2F, 0x1E, 0xFD, 0x0F, 0xE0 // 41 46 53 2F 1E FD 0F E0
#define SYSTEM256_NVM_JAPAN_IDENTIFIER 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
#define DEFREG SYSTEM256_NVM_ASIA5_IDENTIFIER
u8 ForcedRegion[8] = {DEFREG};

#define REGION_FMT "{%02X %02X %02X %02X %02X %02X %02X %02X}"
#define REGION_ARGS(x) x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]

static int get_region_override() {
    int fd = open("mc0:ACREGION", O_RDONLY);
    if (fd > 0) {
        if (read(fd, (void*)ForcedRegion, sizeof(ForcedRegion)) == sizeof(ForcedRegion)) {
            printf("acrtc: new fake region " REGION_FMT "\n", REGION_ARGS(ForcedRegion));
        }
		close(fd);
    }
}

static int start_thread(void (*func)(void *arg), int size, int attr, int prio, void *argp)
{
	iop_thread_t thread_param;
	int thid;
	int r;

	thread_param.attr = attr;
	thread_param.thread = func;
	thread_param.priority = prio;
	thread_param.stacksize = size;
	thread_param.option = 0;
	thid = CreateThread(&thread_param);
	if ( thid <= 0 )
	{
		printf("CreateThread (%d)\n", thid);
		return -1;
	}
	r = StartThread(thid, argp);
	if ( r )
	{
		printf("StartThread (%d)\n", r);
		DeleteThread(thid);
		return -1;
	}
	return 0;
}

static void *sce_actest(unsigned int fno, void *data, int size)
{
	int ret;
	acData *datat;

	(void)size;
	datat = (acData *)data;
	switch ( fno )
	{
		case 1:
		{
			ret = sceCdReadClock(&(datat->data.rtc));
			break;
		}
		case 2:
		{
			ret = sceCdWriteClock(&(datat->data.rtc));
			break;
		}
		case 3:
		{
			ret = sceCdRI(datat->data.id, (u32 *)&(datat->ret));
			printf("acrtc: reading ILINKID.\n"
				   "acrtc: original region: " REGION_FMT "\n", REGION_ARGS(datat->data.id));
			memcpy(datat->data.id, (u8*)ForcedRegion, sizeof(ForcedRegion));
			printf("acrtc: new region: " REGION_FMT "\n", REGION_ARGS(datat->data.id));
			break;
		}
		case 4:
		{
			printf("acrtc: warning, game is writing iLink ID: " REGION_FMT "\n", REGION_ARGS(datat->data.id));
			ret = sceCdWI(datat->data.id, (u32 *)&(datat->ret));
			break;
		}
		default:
		{
			printf("sce_hddtest: unrecognized code %x\n", fno);
			ret = -1;
			break;
		}
	}
	*(u32 *)data = ret;
	return data;
}

void sce_hddtest_loop(void *arg)
{
	(void)arg;
	sceSifInitRpc(0);
	sceSifSetRpcQueue(&qd, GetThreadId());
	sceSifRegisterRpc(&sd, 0xFFFF, (SifRpcFunc_t)sce_actest, &buffer, 0, 0, &qd);
	sceSifRpcLoop(&qd);
}

int _start(int argc, char **argv)
{
	(void)argc;
	(void)argv;

	return start_thread(sce_hddtest_loop, 0x1000, 0x2000000, 32, 0) < 0;
}

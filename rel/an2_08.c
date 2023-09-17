#include <common.h>
#include <evt_cmd.h>

#include <spm/dispdrv.h>
#include <spm/evtmgr.h>
#include <spm/evtmgr_cmd.h>
#include <spm/fontmgr.h>
#include <spm/gxsub.h>
#include <spm/item_data.h>
#include <spm/mario_pouch.h>
#include <spm/mario.h>
#include <spm/msgdrv.h>
#include <spm/spmario.h>
#include <spm/spmario_snd.h>
#include <spm/system.h>
#include <spm/wpadmgr.h>
#include <spm/rel/an2_08.h>
#include <wii/cx.h>
#include <wii/gx.h>
#include <msl/stdio.h>
#include <msl/string.h>

static An2_08Work * wp;
static char * lbl_80cdf43c;
const char * lbl_80def2c8;
u32 lbl_80cddef8;
Unk lbl_80cddf00;
Unk lbl_80cdf610;
Unk lbl_80cddf04;
Unk lbl_80def2a8;
Unk lbl_80cddf18;
Unk lbl_80cddf14;
Unk lbl_80cddf08;
Unk lbl_80def2b8;
Unk lbl_80cddf20;
Unk lbl_80cddf58;
Unk lbl_80cddf90;
void func_80028774();
void func_80c76d00();
void func_801561d4();

u32 lbl_80f65660[] = {
    0x00000000, 0x00000000
};

asm UNKNOWN_FUNCTION(func_80c6c908)
{
    #include "asm/80c6c908.s"
}

asm UNKNOWN_FUNCTION(func_80c6c94c)
{
    #include "asm/80c6c94c.s"
}

asm UNKNOWN_FUNCTION(func_80c6cccc)
{
    #include "asm/80c6cccc.s"
}

asm UNKNOWN_FUNCTION(func_80c6ce24)
{
    #include "asm/80c6ce24.s"
}

asm UNKNOWN_FUNCTION(func_80c6ce8c)
{
    #include "asm/80c6ce8c.s"
}

asm UNKNOWN_FUNCTION(func_80c6d584)
{
    #include "asm/80c6d584.s"
}

asm UNKNOWN_FUNCTION(func_80c6d87c)
{
    #include "asm/80c6d87c.s"
}

#include "jumptable/80def2d8.inc"
#include "jumptable/80def300.inc"
#include "jumptable/80def320.inc"
asm UNKNOWN_FUNCTION(func_80c6d894)
{
    #include "asm/80c6d894.s"
}

asm UNKNOWN_FUNCTION(func_80c6f1dc)
{
    #include "asm/80c6f1dc.s"
}

asm UNKNOWN_FUNCTION(func_80c6f244)
{
    #include "asm/80c6f244.s"
}

asm UNKNOWN_FUNCTION(func_80c6f2a8)
{
    #include "asm/80c6f2a8.s"
}

asm UNKNOWN_FUNCTION(func_80c72398)
{
    #include "asm/80c72398.s"
}

asm UNKNOWN_FUNCTION(func_80c7249c)
{
    #include "asm/80c7249c.s"
}

s32 evt_rpg_mario_take_damage(EvtEntry* evtEntry) {
    MarioPouchWork* temp_r3;
    s32 damage;
    EvtVar* args;

    args = evtEntry->pCurData;
    damage = evtGetValue(evtEntry, *args++);
    evtGetValue(evtEntry, *args++);
    temp_r3 = pouchGetPtr();
    temp_r3->hp -= damage;
    if (temp_r3->hp <= 0) {
        temp_r3->hp = 0;
        wp->unk_54 |= 0x8000;
    }
    evtSetValue(evtEntry, *args++, 0);
    return 2;
}

asm UNKNOWN_FUNCTION(func_80c725c0)
{
    #include "asm/80c725c0.s"
}

asm UNKNOWN_FUNCTION(func_80c72620)
{
    #include "asm/80c72620.s"
}

asm UNKNOWN_FUNCTION(func_80c72680)
{
    #include "asm/80c72680.s"
}

asm UNKNOWN_FUNCTION(func_80c726b8)
{
    #include "asm/80c726b8.s"
}

asm UNKNOWN_FUNCTION(func_80c72764)
{
    #include "asm/80c72764.s"
}

asm UNKNOWN_FUNCTION(func_80c72900)
{
    #include "asm/80c72900.s"
}

asm UNKNOWN_FUNCTION(func_80c72a54)
{
    #include "asm/80c72a54.s"
}

asm UNKNOWN_FUNCTION(func_80c72b38)
{
    #include "asm/80c72b38.s"
}

asm UNKNOWN_FUNCTION(func_80c72c00)
{
    #include "asm/80c72c00.s"
}

asm UNKNOWN_FUNCTION(func_80c72c40)
{
    #include "asm/80c72c40.s"
}

asm UNKNOWN_FUNCTION(func_80c72c78)
{
    #include "asm/80c72c78.s"
}

asm UNKNOWN_FUNCTION(func_80c72cf8)
{
    #include "asm/80c72cf8.s"
}

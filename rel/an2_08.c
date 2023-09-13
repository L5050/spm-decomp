#include <common.h>
#include <evt_cmd.h>
#include <spm/evtmgr.h>
#include <spm/evtmgr_cmd.h>
#include <spm/rel/an2_08.h>

extern An2_08Work * lbl_80f65660;

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
    MarioPouchWork* marioPouchWork;
    s32 damage;
    EvtVar* args;

    args = evtEntry->pCurData;
    damage = evtGetValue(evtEntry, *args++);
    evtGetValue(evtEntry, *args++);
    marioPouchWork = pouchGetPtr();
    marioPouchWork->hp -= damage;
    if (marioPouchWork->hp <= 0) {
        marioPouchWork->hp = 0;
        lbl_80f65660->unk_54 |= 0x8000;
    }
    evtSetValue(evtEntry, *args++, 0);
    return EVT_RET_CONTINUE;
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

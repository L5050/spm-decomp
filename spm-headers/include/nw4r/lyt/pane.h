#pragma once

#include <common.h>
#include <msl/new.h>
#include <nw4r/lyt/animation.h>
#include <nw4r/lyt/resourceAccessor.h>

namespace nw4r {
namespace lyt {

class Pane
{
public:
    virtual ~Pane();
    virtual UNKNOWN_FUNCTION(GetRuntimeTypeInfo);
    virtual UNKNOWN_FUNCTION(CalculateMtx);
    virtual UNKNOWN_FUNCTION(Draw);
    virtual UNKNOWN_FUNCTION(DrawSelf);
    virtual UNKNOWN_FUNCTION(Animate);
    virtual UNKNOWN_FUNCTION(AnimateSelf);
    virtual UNKNOWN_FUNCTION(GetVtxColor);
    virtual UNKNOWN_FUNCTION(SetVtxColor);
    virtual UNKNOWN_FUNCTION(GetColorElement);
    virtual UNKNOWN_FUNCTION(SetColorElement);
    virtual UNKNOWN_FUNCTION(GetVtxColorElement);
    virtual UNKNOWN_FUNCTION(SetVtxColorElement);
    virtual Pane * FindPaneByName(const char * findName, bool bRecursive);
    virtual UNKNOWN_FUNCTION(FindMaterialByName);
    virtual UNKNOWN_FUNCTION(BindAnimation);
    virtual UNKNOWN_FUNCTION(UnbindAnimation_1);
    virtual UNKNOWN_FUNCTION(UnbindAllAnimation);
    virtual UNKNOWN_FUNCTION(UnbindAnimationSelf);
    virtual UNKNOWN_FUNCTION(FindAnimationLinkSelf);
    virtual UNKNOWN_FUNCTION(SetAnimationEnable);
    virtual UNKNOWN_FUNCTION(GetMaterial);
    virtual UNKNOWN_FUNCTION(LoadMtx);

    u8 unknown_0x4[0xd4 - 0x4];
};
SIZE_ASSERT(Pane, 0xd4)

} // namespace lyt
} // namespace nw4r

"""
Creates a build script for ninja
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import StringIO
import json
import os
import re
from typing import List, Tuple

from ninja_syntax import Writer

import common as c

####################
# Setup Validation #
####################

# Check CW was added
assert os.path.exists("tools/4199_60831/mwcceppc.exe") and \
       os.path.exists("tools/4199_60831/mwldeppc.exe"), \
       "Error: Codewarrior not found in tools/4199_60831"

# Check binaries were added
assert os.path.exists(c.DOL) and os.path.exists(c.REL), \
       "Error: Base binaries not found"

# Check binaries are correct
dol_hash = c.get_file_sha1(c.DOL)
assert dol_hash == bytes.fromhex("3fd3d9815528d1c04bc433d67d273b1e3301e976"), \
       "Error: Base dol hash isn't correct."
rel_hash = c.get_file_sha1(c.REL)
if rel_hash == bytes.fromhex("29c78007559996dee6b615005fa3369d4cc1f5e3"):
    assert 0, "Error: Base rel is from PAL revision 1, the decomp currently requires revision 0"
else:
    assert rel_hash == bytes.fromhex("9b9b92c370b1aab68cf6ff5a3eb824fdab6a55ff")

# Check submodules added
assert os.path.exists(c.PPCDIS), \
       "Error: Git submodules not initialised"

###############
# Ninja Setup #
###############

outbuf = StringIO()
n = Writer(outbuf)
n.variable("ninja_required_version", "1.3")
n.newline()

################
# Project Dirs #
################

n.variable("builddir", c.BUILDDIR)
n.variable("outdir", c.OUTDIR)
n.variable("orig", c.ORIG)
n.variable("tools", c.TOOLS)
n.variable("config", c.CONFIG)
n.newline()

#########
# Tools #
#########

n.variable("python", c.PYTHON)
n.variable("ppcdis", c.PPCDIS)
n.variable("analyser", c.ANALYSER)
n.variable("disassembler", c.DISASSEMBLER)
n.variable("orderstrings", c.ORDERSTRINGS)
n.variable("orderfloats", c.ORDERFLOATS)
n.variable("elf2dol", c.ELF2DOL)
n.variable("elf2rel", c.ELF2REL)
n.variable("codewarrior", c.CODEWARRIOR)
n.variable("cc", c.CC)
n.variable("ld", c.LD)
n.variable("devkitppc", c.DEVKITPPC)
n.variable("as", c.AS)
n.variable("iconv", c.ICONV)
n.newline()

##############
# Tool flags #
##############

n.variable("sda", c.SDA)
n.variable("asflags", c.ASFLAGS)
n.variable("ldflags", c.LDFLAGS)
n.variable("ppcdis_rel_flags", c.PPCDIS_REL_FLAGS)
n.variable("ppcdis_analysis_flags", c.PPCDIS_ANALYSIS_FLAGS)
n.variable("ppcdis_disasm_flags", c.PPCDIS_DISASM_FLAGS)
n.newline()

#########
# Rules #
#########

# Windows can't use && without this
ALLOW_CHAIN = "cmd /c " if os.name == "nt" else ""

n.rule(
    "analyse",
    command = "$analyser $in $sda $out $analysisflags",
    description = "ppcdis analysis $in",
    pool="console"
)

n.rule(
    "disasm_slice",
    command = "$disassembler $in $sda $out -q $disasmflags -s $slice",
    description = "ppcdis disassembly $out",
)

n.rule(
    "disasm_single",
    command = "$disassembler $in $sda $out -f $addr -i -q $disasmflags",
    description = "ppcdis function disassembly $addr"
)

n.rule(
    "jumptable",
    command = "$disassembler $in $sda $out -j $addr -q $disasmflags",
    description = "Jumptable $addr"
)

n.rule(
    "orderstrings",
    command = "$orderstrings $in $addrs $out $flags --enc shift-jis",
    description = "Order strings $in $addrs"
)

n.rule(
    "orderfloats",
    command = "$orderfloats $in $addrs $out $flags",
    description = "Order floats $in $addrs"
)

n.rule(
    "elf2dol",
    command = "$elf2dol $in -o $out",
    description = "elf2dol $in"
)

n.rule(
    "elf2rel",
    command = "$elf2rel $in -o $out $flags",
    description = "elf2rel $in"
)

n.rule(
    "sha1sum",
    command = ALLOW_CHAIN + "sha1sum -c $in && touch $out",
    description = "Verify $in",
    pool="console"
)

n.rule(
    "as",
    command = f"$as $asflags -I {c.INCDIR} -I {c.PPCDIS_INCDIR} -c $in -o $out -I orig",
    description = "AS $in"
)

# Due to CW dumbness with .d output location, $outstem must be defined without the .o
n.rule(
    "cc",
    command = f"$cc $cflags -MD -gccdep -c $in -o $out",
    description = "CC $in",
    deps = "gcc",
    depfile = "$outstem.d"
)

n.rule(
    "ccs",
    command = f"$cc $cflags -MD -gccdep -c $in -o $out -S",
    description = "CC -S $in",
    deps = "gcc",
    depfile = "$outstem.d"
)

n.rule(
    "ld",
    command = "$ld $ldflags -map $map -lcf $lcf $in -o $out",
    description = "LD $out",
)

n.rule(
    "iconv",
    command = "$iconv $in $out",
    description = "iconv $in",
)

###########
# Sources #
###########

@dataclass
class SourceContext:
    srcdir: str
    cflags: str
    binary: str
    labels: str
    relocs: str
    slices: str
    sdata2_threshold: int
    binflags: str = ""

class GeneratedInclude(ABC):
    def __init__(self, source_name: str, path: str):
        self.source_name = source_name
        self.path = path

    @abstractmethod
    def build(self, ctx: SourceContext):
        raise NotImplementedError

    def find(source_name: str, txt: str) -> List["GeneratedInclude"]:
        return [
            cl(source_name, match)
            for cl in (
                AsmInclude,
                JumptableInclude,
                StringInclude,
                FloatInclude,
                DoubleInclude
            )
            for match in re.findall(cl.REGEX, txt)
        ]

class AsmInclude(GeneratedInclude):
    REGEX = r'#include "asm\/([0-9a-f]{8})\.s"'

    def __init__(self, source_name: str, match: str):
        self.addr = match
        super().__init__(source_name, f"{c.BUILD_INCDIR}/asm/{self.addr}.s")

    def build(self, ctx: SourceContext):
        n.build(
            self.path,
            rule="disasm_single",
            inputs=[ctx.binary, ctx.labels, ctx.relocs],
            implicit=[c.SYMBOLS, c.DISASM_OVERRIDES],
            variables={
                "disasmflags" : f"$ppcdis_disasm_flags {ctx.binflags} -n {self.source_name}",
                "addr" : self.addr
            }
        )
    
    def __repr__(self):
        return f"AsmInclude({self.addr})"

class JumptableInclude(GeneratedInclude):
    REGEX = r'#include "jumptable\/([0-9a-f]{8})\.inc"'

    def __init__(self, source_name: str, match: str):
        self.addr = match
        super().__init__(source_name, f"{c.BUILD_INCDIR}/jumptable/{self.addr}.inc")

    def build(self, ctx: SourceContext):
        n.build(
            self.path,
            rule="jumptable",
            inputs=[ctx.binary, ctx.labels, ctx.relocs],
            implicit=[c.SYMBOLS, c.DISASM_OVERRIDES],
            variables={
                "disasmflags" : f"$ppcdis_disasm_flags {ctx.binflags} -n {self.source_name}",
                "addr" : self.addr
            }
        )

    def __repr__(self):
        return f"JumptableInclude({self.addr})"

class StringInclude(GeneratedInclude):
    REGEX = r'#include "orderstrings\/([0-9a-f]{8})_([0-9a-f]{8})\.inc"'

    def __init__(self, source_name: str, match: Tuple[str]):
        self.start, self.end = match
        super().__init__(source_name, f"{c.BUILD_INCDIR}/orderstrings/{self.start}_{self.end}.inc")

    def build(self, ctx: SourceContext):
        n.build(
            self.path,
            rule="orderstrings",
            inputs=ctx.binary,
            variables={
                "addrs" : f"{self.start} {self.end}",
                "flags" : ctx.binflags
            }
        )

    def __repr__(self):
        return f"StringInclude({self.start}, {self.end})"

class FloatInclude(GeneratedInclude):
    REGEX = r'#include "(orderfloats(m?))\/([0-9a-f]{8})_([0-9a-f]{8})\.inc"'

    def __init__(self, source_name: str, match: Tuple[str]):
        folder, manual, self.start, self.end = match
        self.manual = manual != ''
        super().__init__(source_name, f"{c.BUILD_INCDIR}/{folder}/{self.start}_{self.end}.inc")

    def build(self, ctx: SourceContext):
        sda = "--sda " if ctx.sdata2_threshold >= 4 else ""
        asm = "" if self.manual else "--asm"
        n.build(
            self.path,
            rule="orderfloats",
            inputs=ctx.binary,
            variables={
                "addrs" : f"{self.start} {self.end}",
                "flags" : f"{ctx.binflags} {sda} {asm}"
            }
        )

    def __repr__(self):
        return f"FloatInclude({self.start}, {self.end})"

class DoubleInclude(GeneratedInclude):
    REGEX = r'#include "orderdoubles\/([0-9a-f]{8})_([0-9a-f]{8})\.inc"'

    def __init__(self, source_name: str, match: Tuple[str]):
        self.start, self.end = match
        super().__init__(source_name, f"{c.BUILD_INCDIR}/orderdoubles/{self.start}_{self.end}.inc")

    def build(self, ctx: SourceContext):
        n.build(
            self.path,
            rule="orderfloats",
            inputs=ctx.binary,
            variables={
                "addrs" : f"{self.start} {self.end}",
                "flags" : f"{ctx.binflags} --double"
            }
        )

    def __repr__(self):
        return f"DoubleInclude({self.start}, {self.end})"

class Source(ABC):
    def __init__(self, decompiled: bool, src_path: str, o_path: str,
                 gen_includes: List[GeneratedInclude] = []):
        self.decompiled = decompiled
        self.src_path = src_path
        self.o_path = o_path
        self.o_stem = o_path[:-2]
        self.gen_includes = gen_includes

    def build(self):
        raise NotImplementedError
    
    def make(ctx: SourceContext, source: c.SourceDesc):
        if isinstance(source, str):
            ext = source.split('.')[-1].lower()
            if ext in ("c", "cpp", "cxx", "cc"):
                return CSource(ctx, source)
            elif ext == "s":
                return AsmSource(ctx, source)
            else:
                assert 0, f"Unknown source type .{ext}"
        else:
            return GenAsmSource(ctx, *source)

class GenAsmSource(Source):
    def __init__(self, ctx: SourceContext, section: str, start: int, end: int):
        self.start = start
        self.end = end
        self.ctx = ctx
        src_path = f"$builddir/asm/{section}_{start:x}_{end:x}.s"
        super().__init__(False, src_path, src_path + ".o")

    def build(self):
        n.build(
            self.src_path,
            rule = "disasm_slice",
            inputs = [self.ctx.binary, self.ctx.labels, self.ctx.relocs],
            implicit = [c.SYMBOLS, c.DISASM_OVERRIDES],
            variables = {
                "slice" : f"{self.start:x} {self.end:x}",
                "disasmflags" : f"$ppcdis_disasm_flags {self.ctx.binflags}"
            }
        )
        n.build(
            self.o_path,
            rule="as",
            inputs=self.src_path
        )

class AsmSource(Source):
    def __init__(self, ctx: SourceContext, path: str):
        super().__init__(True, path, f"$builddir/{path}.o")

    def build(self):
        n.build(
            self.o_path,
            rule = "as",
            inputs = self.src_path
        )


class CSource(Source):
    def __init__(self, ctx: SourceContext, path: str):
        self.cflags = ctx.cflags
        self.iconv_path = f"$builddir/iconv/{path}"

        # Find generated includes
        with open(path, encoding="utf-8") as f:
            gen_includes = GeneratedInclude.find(path, f.read())

        self.s_path = f"$builddir/{path}.s"
        super().__init__(True, path, f"$builddir/{path}.o", gen_includes)

    def build(self):
        n.build(
            self.iconv_path,
            rule="iconv",
            inputs=self.src_path
        )
        n.build(
            self.o_path,
            rule = "cc",
            inputs = self.iconv_path,
            implicit = [inc.path for inc in self.gen_includes],
            variables = {
                "cflags" : self.cflags,
                "outstem" : self.o_stem
            }
        )
        # Optional manual debug target
        n.build(
            self.s_path,
            rule = "ccs",
            inputs = self.iconv_path,
            implicit = [inc.path for inc in self.gen_includes],
            variables = {
                "cflags" : self.cflags,
                "outstem" : self.o_stem
            }
        )

def load_sources(ctx: SourceContext):
    raw = c.get_cmd_stdout(
        f"{c.SLICES} {ctx.binary} {ctx.slices} {ctx.binflags} -o -p {ctx.srcdir}/"
    )
    return [Source.make(ctx, s) for s in json.loads(raw)]

dol_ctx = SourceContext(c.DOL_SRCDIR, c.DOL_CFLAGS, c.DOL, c.DOL_LABELS,
                        c.DOL_RELOCS, c.DOL_SLICES, 4)
rel_ctx = SourceContext(c.REL_SRCDIR, c.REL_CFLAGS, c.REL, c.REL_LABELS,
                        c.REL_RELOCS, c.REL_SLICES, 0, c.PPCDIS_REL_FLAGS)

dol_sources = load_sources(dol_ctx)
dol_c_sources = [source for source in dol_sources if isinstance(source, CSource)]
dol_gen_includes = [inc for source in dol_c_sources for inc in source.gen_includes]

rel_sources = load_sources(rel_ctx)
rel_c_sources = [source for source in rel_sources if isinstance(source, CSource)]
rel_gen_includes = [inc for source in rel_c_sources for inc in source.gen_includes]

##########
# Builds #
##########

n.build(
    [c.REL_LABELS, c.REL_RELOCS],
    rule = "analyse",
    inputs = c.REL,
    implicit = c.ANALYSIS_OVERRIDES,
    variables = {
        "analysisflags" : "$ppcdis_rel_flags $ppcdis_analysis_flags"
    }
)

n.build(
    [c.DOL_LABELS, c.DOL_RELOCS],
    rule = "analyse",
    inputs = c.DOL,
    implicit = [c.ANALYSIS_OVERRIDES, c.REL_LABELS],
    variables = {
        "analysisflags" : f"$ppcdis_analysis_flags -l {c.REL_LABELS}"
    }
)

for inc in dol_gen_includes:
    inc.build(dol_ctx)

for inc in rel_gen_includes:
    inc.build(rel_ctx)

for source in dol_sources + rel_sources:
    source.build()

n.build(
    c.DOL_ELF,
    rule="ld",
    inputs=[s.o_path for s in dol_sources],
    implicit=c.DOL_LCF,
    implicit_outputs=c.DOL_MAP,
    variables={
        "map" : c.DOL_MAP,
        "lcf" : c.DOL_LCF
    }
)

n.build(
    c.DOL_OUT,
    rule="elf2dol",
    inputs=c.DOL_ELF,
)

n.build(
    "$builddir/main.dol.ok",
    rule = "sha1sum",
    inputs = c.DOL_SHA,
    implicit = c.DOL_OUT,
)
n.default("$builddir/main.dol.ok")

n.build(
    c.REL_PLF,
    rule="ld",
    inputs=[s.o_path for s in rel_sources],
    implicit=c.REL_LCF,
    implicit_outputs=c.REL_MAP,
    variables={
        "map" : c.REL_MAP,
        "lcf" : c.REL_LCF,
        "ldflags" : c.LDFLAGS + " -r1"
    }
)

n.build(
    c.REL_OUT,
    rule="elf2rel",
    inputs=[c.REL_PLF, c.DOL_ELF],
    variables={
        "flags" : f"-n 18 -r {c.REL} -a {c.REL_ADDR} -b {c.REL_BSS}"
    }
)

n.build(
    "$builddir/relF.rel.ok",
    rule = "sha1sum",
    inputs = c.REL_SHA,
    implicit = c.REL_OUT,
)
n.default("$builddir/relF.rel.ok")

##########
# Ouptut #
##########

with open("build.ninja", 'w') as f:
    f.write(outbuf.getvalue())
n.close()

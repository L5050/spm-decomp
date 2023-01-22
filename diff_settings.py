from argparse import ArgumentParser, Namespace
import common as c

def apply(config, args: Namespace):
    if args.rel:
        config["mapfile"] = c.REL_MAP
        config["myimg"] = c.REL_PLF
        config["baseimg"] = c.REL_EXPECTED
        config["source_directories"] = [c.REL_SRCDIR, *c.INCDIRS]
    else:
        config["mapfile"] = c.DOL_MAP
        config["myimg"] = c.DOL_ELF
        config["baseimg"] = c.DOL_EXPECTED
        config["source_directories"] = [c.DOL_SRCDIR, *c.INCDIRS]
    config["make_command"] = ["ninja"]
    config["makeflags"] = []
    config["arch"] = "ppc"
    config["map_format"] = "mw"
    config["build_dir"] = c.BUILDDIR
    config["expected_dir"] = c.EXPECTED
    config["objdump_executable"] = c.OBJDUMP
    config["show_line_numbers_default"] = True

def add_custom_arguments(parser: ArgumentParser):
    parser.add_argument("-r", "--rel", action="store_true", help="(SPM) Diff a function in relF.rel")

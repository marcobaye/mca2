#!/usr/bin/env python3

import conv
import os
import subprocess
import sys

architectures = {
    "c64":          "arch64.a",
    "c128":         "arch128.a",
    "plus4":        "arch264.a",
    "steckschwein": "archsw.a",
}

def set_arch(arch_arg):
    archfile = architectures.get(arch_arg, None)
    if archfile is None:
        print("Unknown architecture. Supported architectures are:", file=sys.stderr)
        for key in architectures.keys():
            print("\t", key, file=sys.stderr)
        sys.exit(1)
    return archfile

def appdir(file=None):
    """find path to actual binary, so we can use it to refer to files in repo."""
    prog = sys.argv[0]
    realpath = os.path.realpath(prog)   # now without symlinks
    appdir = os.path.dirname(realpath)
    if file is None:
        return appdir
    return os.path.join(appdir, file)

def convert(infile, outfile):
    con = conv.converter()
    con.parse_file(infile)
    # redirect stdout to file, call convertor, restore stdout:
    temp = sys.stdout
    sys.stdout = open(outfile, "wt")
    con.output()
    sys.stdout = temp

def assemble(archfile, gamefile, outfile):
    #print("arch file:", archfile)
    #print("acme file:", gamefile)
    #print("outfile:", outfile)
    # build arguments for ACME:
    cliargs = ["acme", "--format", "plain", "--outfile", outfile, "-v2", "-Wtype-mismatch", appdir("6502src/" + archfile), gamefile]
    # add other source files from application directory (order is important: mca first, tail last, engine before output)
    cliargs.extend([appdir("6502src/mca2.a"), appdir("6502src/charset.a"), appdir("6502src/engine.a"), appdir("6502src/output.a"), appdir("6502src/tail.a")])
    # now call ACME:
    print(" ".join(cliargs))
    subprocess.check_call(cliargs)


if __name__ == '__main__':
    sys.exit("This file is a library, it cannot be run.")

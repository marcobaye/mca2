#!/usr/bin/env python3

import argparse
import backend
import sys

def main():
    # if run without arguments, show help instead of complaining:
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    parser = argparse.ArgumentParser(allow_abbrev = False, description =
"""
This program converts MCA2 game description files into executables.
""")
    parser.add_argument("-a", "--arch", metavar="ARCH", type=str, help="target architecture", default="c64")
    parser.add_argument("-o", "--outfile", metavar="OUTFILE", type=str, help="output file name", default="out.prg")
    parser.add_argument("file", metavar="INFILE", help="Game description file.")
    args = parser.parse_args()
    archfile = backend.set_arch(args.arch.lower())
    gamefile = args.file + ".tmp.a"
    print("Trying to convert", args.file, "to", gamefile, "...")
    backend.convert(args.file, gamefile)
    print("Trying to assemble ...")
    backend.assemble(archfile, gamefile, args.outfile)

if __name__ == '__main__':
    main()

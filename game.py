#!/bin/cat
# this is no python source, the file is only
# called *.py to have syntax coloring!

# see "example.py" for help about the command syntax in this file.

# symbolic constants:
define FALSE	0
define TRUE	1

# variables and default values:
var score	0

# items:
# (args are size, start location, skript name, game name, game description)
item small start palawaum "Palawaum" "ein normaler Palawaum aus sieben Banuzen"

# "asm" passes the remainder of the line to the assembler backend unchanged:
# these two are used for colored text output
asm HINZ	= petscii_YELLOW	# puts "HINZ = petscii_YELLOW" into output file
asm KUNZ	= petscii_LRED
# ONLY USE THIS FOR SYMBOL DEFINITIONS, NOT FOR ACTUAL MACHINE CODE!

# usages:
#using ITEM1 ITEM2

# procedures:
#defproc name

# locations:
loc start
	"Das Spiel startet hier, weil dieser Ort 'start' heisst."
	s2 anderswo

loc anderswo
	"Dies ist ein anderer Ort."

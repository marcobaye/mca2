#!/bin/cat
# this file is only called *.py to have python syntax coloring!

# new file format to describe situations:
# file is parsed line-by-line
# hash character indicates comments
	# leading whitespace is ignored? or use indentation as block delimiter?

# first non-whitespace char determines type of line:
# +	new situation
# "	print text (you can use symbolic petscii codes)
# d	set target for "down"
# dec	decrement variable	FIXME - allow underrun?
# e	set target for "east"
# enum TOT, LEBENDIG, UNTOT	define symbolic constants	FIXME - this clashes with telling vars/literals apart!
# if	start conditional block
# inc	increment variable	FIXME - allow overrun?
# n	set target for "north"
# s	set target for "south"
# u	set target for "up"
# w	set target for "west"
# v	declare uint16 variable and default value ("current_sit" is pre-defined and must be read-only!)
	# this would allow to load/save current state just by loading/saving var block!
# VAR=LITERAL	set variable to fixed value
# VAR=OTHERVAR	copy var
# FIXME - internally, convert literals to vars? makes things easier!

# example:

# '+' starts a new situation, arg is name (FIXME - just use "no indent" instead of '+'?)
+ deck4_transporter_room
	# '"' starts text to output (implicit PRINT)
	"You are in what looks like a transporter room right out of Star Trek.", cr
	"There is a corridor to the north, a turbolift to the east, and an opening to a vertical Jefferies tube."
	# "nsewud" characters indicate target situations for north/south/east/west/up/down
	# "nsowhr" auf deutsch (nord/süd/ost/west/hoch/runter)
	n corridor_transp_room
	e turbolift
	u deck3_jefferies
	d deck5_jefferies
	# => this will make the game display n/e/u/d as possible directions and s/w as impossible
FIXME - add shorthand command for "alternative action leading to new situation"?
	# 'a' is for alternative actions, with key, text and result as arguments
	# remember "nsewud" cannot be used ("nsowhr" if german), so better use digits!
	a

	# still to do:
	# inc VAR
	# dec VAR
	# VAR=LITERAL
	# if VAR = LITERAL	# or '<' or '>'
	#	code
	# endif
	# "restart" to set vars to default?
	# call some_assembler_label	# call assembler subroutine (to beep, shake screen, etc.)

#!/bin/cat
# this file is only called *.py to have python syntax coloring!
 
# new file format to describe situations:
# file is parsed line-by-line
# hash character indicates comments
	# leading whitespace is ignored

# first non-whitespace char determines type of line:
# sit	new situation
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

# 'sit' starts a new situation, arg is name
sit start	# <= one situation MUST be called "start", this is where the game begins
	"Hi! Hit the correct key to begin the game."
	a corridor2

# "forward" rooms
sit ready_room
	"You are in the Captain's ready room."

sit bridge
	"You are on the bridge of the starship. There are doors facing west, east and south."
	w2 ready_room
	e2 bathroom
	s2 corridor1

sit bathroom
	"You are in a bathroom. There are three sea shells visible."

# corridor, forward
sit captains_quarters
	"You are in what looks like the Captain's quarters."

sit corridor1
	"You are at the northern end of a corridor. There are doors to the north, east and west."
	we2 captains_quarters room1e

sit room1e
	"An empty room."

# corridor, middle
sit room2w
	"An empty room."

sit corridor2
	"You are in a corridor. There are two doors (east and west)."
	ns2 corridor1 corridor3
	we2 room2w room2e

sit room2e
	"An empty room."

# corridor, back
sit room3w
	"An empty room."

sit corridor3
	""
	we2 room3w room3e

sit room3e
	"An empty room."

# "back" rooms
sit engine_room
	"You are in the engine room."
	n2 corridor3

sit deck4_transporter_room
	# '"' starts text to output (implicit PRINT)
	"You are in what looks like a transporter room right out of Star Trek.", cr
	"There is a corridor to the north, a turbolift to the east, and an opening to a vertical Jefferies tube."
	# "nsewud" characters indicate target situations for north/south/east/west/up/down
	n corridor_transp_room
	e turbolift
	u deck3_jefferies
	d deck5_jefferies
	# => this will make the game display n/e/u/d as possible directions and s/w as impossible
#FIXME - add shorthand command for "alternative action leading to new situation"?
	# 'a' is for alternative actions, with key, text and result as arguments
	# remember "nsewud" cannot be used ("nsowhr" if german), so better use digits!
#	a

	# still to do:
	# inc VAR
	# dec VAR
	# VAR=LITERAL
	# if VAR = LITERAL	# or '<' or '>'
	#	code
	# endif
	# "restart" to set vars to default?
	# call some_assembler_label	# call assembler subroutine (to beep, shake screen, etc.)
#

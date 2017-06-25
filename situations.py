#!/bin/cat
# this file is only called *.py to have python syntax coloring!
 
# new file format to describe situations:
# file is parsed line-by-line
# hash character indicates comments
	# leading whitespace is ignored

# first word (or character) of each line determines the type of line:
# "const" defines symbolic constants:
const DEAD	0
const ALIVE	1
const CLOSED	0
const OPEN	1
const OFFEN	OPEN	# once they are defined, they can be used like numbers
const MOOD_IN_LOVE	0
const MOOD_FRIENDLY	1
const MOOD_NEUTRAL	2
const MOOD_GRUMPY	3
const MOOD_PISSED	4
# "var" defines a game variable and its start value
var dragon	ALIVE
var crocodile	ALIVE
var secretdoor	CLOSED
var dwarfmood	MOOD_NEUTRAL
var lives_left	5
var cows_killed	0
# "sit" starts a new situation, basically a location in the game:
sit deck4_transporter_room
	# lines beginning with double quotes are text to output (basically a PRINT instruction without the "PRINT"):
	"You are in what looks like a transporter room right out of Star Trek.", cr	# "cr" adds a carriage return
	"There is a corridor to the north, a turbolift to the east, and an opening to a vertical Jefferies tube."
	# "nsewud" characters indicate target situations when player attempts to go north/south/east/west/up/down:
	n corridor_transp_room	# going north leads to the "corridor outside the transporter room" stuation
	e turbolift		# going east leads to the turbolift situation
	u deck3_jefferies	# going up leads to "jefferies tube on deck 3" situation
	d deck5_jefferies	# going down leads to "jefferies tube on deck 5" situation
	# ...now the game will display north/east/up/down as possible directions, but neither south nor west

# FIXME - explain this stuff later, do not pile too much on top at once:
	#	north/south, west/east and up/down targets can be given together using ns/we/ud:
	# ud deck3_jefferies deck5_jefferies	# this would specify two targets on a single line
	#	as a convenience function, you can add a "2" to the command to enforce a two-way connection:
	# n2 corridor_transp_room	# this says "going east leads to corridor_transp_room, and going west
	# from there would lead back here again! this way
	#	AND GOING WEST FROM THERE would lead back here again
#FIXME - add shorthand command for "alternative action leading to new situation"?
	# 'a' is for alternative actions, with key, text and result as arguments
	# remember "nsewud" cannot be used ("nsowhr" if german), so better use digits!
#	a


# "TEXT"	print text (you can use symbolic petscii codes)
# n TARGET	set target for "north" direction
	# use s/w/e/u/d for south/west/east/up/down
# dec	decrement variable	FIXME - allow underrun?
# enum TOT, LEBENDIG, UNTOT	define symbolic constants	FIXME - this clashes with telling vars/literals apart!
# if	start conditional block
# inc	increment variable	FIXME - allow overrun?
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

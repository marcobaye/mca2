#!/bin/cat
# this is no python source, the file is only
# called *.py to have syntax coloring!

# simple file format to describe game:
# file is parsed line-by-line
# keywords and symbols are delimited by whitespace
# hash character indicates comments
	# leading whitespace is ignored
/*
you can also use c-style multi-line comment characters
to quickly disable large portions of this file.
*/

# first word (or character) of each line determines the type of line:

# "define" defines symbolic constants (actually the line just registers a text substitution)
# (writing them in upper case is just a convention and not required):
define DEAD	0
define ALIVE	1
define CLOSED	0
define OPEN	1
define OFFEN	OPEN	# once they are defined, constants can be used like numbers
# all calculations are done as unsigned 16-bit integers,
# so numbers must be in 0..65535 range. Negative numbers are not supported, but who needs them anyway?

# "enum" is a faster way to define several symbolic constants at a time:
enum FIST	ROCK	KNIFE	SWORD	PISTOL	LIGHTSABER	# this will assign values 0/1/2/3/4/5
enum MOOD_IN_LOVE	MOOD_FRIENDLY	MOOD_NEUTRAL	MOOD_GRUMPY	MOOD_PISSED	# assigns 0/1/2/3/4
# (these lines have exactly the same effect as separate "define"-lines would have had)

# "var" defines a game variable and its start value:
var dragon	ALIVE
var crocodile	ALIVE
var secretdoor	CLOSED
var dwarfmood	MOOD_NEUTRAL
var lives_left	5
var cows_killed	0

# "asm" lines are passed to assembler backend unchanged:
asm HINZ	= petscii_YELLOW
asm KUNZ	= petscii_LRED
# ONLY USE THIS FOR SYMBOL DEFINITIONS, NOT FOR ACTUAL CODE!

# "loc" starts a new location description:
loc deck4_transporter_room
	# lines beginning with single or double quotes are text to output.
	# You can use predefined petscii codes. "cr" adds a carriage return. Do NOT add null terminator!
	"You are in what looks like a transporter room right out of ", petscii_WHITE, "Star Trek", petscii_GREEN, ".", cr
	"There is a corridor to the north, a turbolift to the east, and an opening to a vertical Jefferies tube."
	"To output double quotes, put them in single quotes as a separate character:", '"', cr
	"", petscii_REVSON, "<= if you want a line to start with a control code, put an empty string before it."
	# "nsewud" characters indicate target locations when player attempts to go north/south/east/west/up/down:
	n corridor_transp_room	# going north leads to the "corridor outside the transporter room" stuation
	e turbolift		# going east leads to the turbolift location
	u deck3_jefferies	# going up leads to "jefferies tube on deck 3" location
	d deck5_jefferies	# going down leads to "jefferies tube on deck 5" location
	# ...now the game will display north/east/up/down as possible directions,
	# but neither south nor west.
	# as a convenience function, you can add a "2" to the command to enforce a two-way connection:
	# n2 corridor_transp_room	# this says "going east leads to corridor_transp_room,
	# AND going west from there would lead back here again!

	#FIXME - add shorthand command for "alternative action leading to new location"?
	# 'a' is for alternative actions, with key, text and result as arguments
	# remember "nsewud" cannot be used ("nsowhr" if german), so better use digits!
#	a


# dec	decrement variable	FIXME - allow underrun?
# if	start conditional block
# inc	increment variable	FIXME - allow overrun?
# v	declare uint16 variable and default value ("HERE" is pre-defined and must be read-only!)
	# this would allow to load/save current state just by loading/saving var block!
# VAR = LITERAL	set variable to fixed value
# VAR = OTHERVAR	copy var
# FIXME - internally, convert literals to vars? makes things easier!

# example:

# 'loc' starts a new location, arg is name
loc start	# <= one location MUST be called "start", this is where the game begins
	"Hi! Hit the correct key to begin the game.", cr
	#a corridor2		FIXME - implement "a"!
	d corridor2

/* this example file uses a starship,
here is the floor plan:

         bridge
           |
 quart - corr1 - toilet
           |
transp - corr2 - airlock
           |
 empty - corr3 - storage
           |
         drive

all connections use the two-way feature, therefore we only specify connections
for north and east directions:
*/

# bridge
loc bridge
	"You are on the bridge of the starship. There is a door facing south."
	# no need to specify south connection, we do that from the other end!

# forward
loc quarters
	"You are in what looks like the Captain's living quarters."
	e2 corridor1	# connect to corridor and back

loc corridor1
	"You are at the northern end of a corridor. There are doors to the north, east and west."
	n2 bridge	# connect to bridge and back
	e2 toilet	# connect to bathroom and back

loc toilet
	"You are in a bathroom. There are three sea shells visible."
	# no need to specify connection as it is done from the other end
	dec lives_left

# middle
loc transporter_room
	"You are in a room with what looks like some kind of teleportation pod."
	e2 corridor2	# connect to corridor and back
	inc cows_killed

loc corridor2
	"You are in a corridor leading north and south. There are two doors (east and west)."
	n2 corridor1
	e2 airlock

loc airlock
	"You are in a downward-facing airlock. The outer door is closed."
	# no need to specify connection as it is done from the other end.
	if dragon == ALIVE
		" The dragon is alive."
	elif dwarfmood != MOOD_PISSED
		" The dwarf is pissed."
	# FIXME - check all comparisons, make sure they work as intended!
	elif secretdoor < CLOSED
		" The secret door < closed."
	elif secretdoor <= OFFEN
		" The secret door <= open."
	elif secretdoor > CLOSED
		" The secret door > closed."
	elif secretdoor >= OFFEN
		" The secret door >= open."
	else
		" This is the ELSE block."
	endif

# corridor, back
loc empty
	"This room seems to be completely empty."
	e2 corridor3	# connect to corridor and back
	if dwarfmood == MOOD_IN_LOVE
		" The dwarf is in love!"
	elif dwarfmood == MOOD_FRIENDLY
		" The dwarf is friendly."
	elif dwarfmood == MOOD_NEUTRAL
		" The dwarf is neutral."
	elif dwarfmood == MOOD_GRUMPY
		" The dwarf is grumpy."
	elif dwarfmood == MOOD_PISSED
		" The dwarf is pissed."
	else
		" The dwarf's mood is off the scale, allowing you to go north!"
		n transporter_room
	endif
	inc dwarfmood	# var=var+1, dwarf's mood is now worse!

loc corridor3
	"You are at the southern end of a corridor. There are doors to the south, east and west."
	n2 corridor2
	e2 storage

loc storage
	"There are some storage containers in this room."
	# no need to specify connection as it is done from the other end.
	dwarfmood = MOOD_IN_LOVE	# assigment to variable

# "back" room
loc engine_room
	"You are in the engine room."
	n2 corridor3

	# still to do:
	# "restart" to set vars to default?
#

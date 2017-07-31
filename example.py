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
enum	FIST	ROCK	KNIFE	SWORD	PISTOL	LIGHTSABER	# this will assign values 0/1/2/3/4/5
enum	MOOD_IN_LOVE	MOOD_FRIENDLY	MOOD_NEUTRAL	MOOD_GRUMPY	MOOD_PISSED	# assigns 0/1/2/3/4
# (these lines have exactly the same effect as separate "define"-lines would have had)

# "var" defines a game variable (16 bit unsigned int) and its start value:
var dragon	ALIVE
var crocodile	ALIVE
var secretdoor	CLOSED
var dwarfmood	MOOD_NEUTRAL
var lives_left	5
var cows_killed	0
# the engine pre-defines a variable called __TMP__, this is needed for internal
# calculations, so DO NOT USE IT YOURSELF!

# "item" defines a game item the player can interact with:
# parameters are size (small/large), start location in game, in-script name, in-game name, in-game description
# small items can be taken by player (put into inventory), large items can only be moved around by code
# in-script names must be unique, in-game names can be re-used (so player thinks it's the same item)
item small NOWHERE	string	"Sehne"		"eine Bogensehne"	#
item small INVENTORY	bow1	"Bogen"		"kaputter Bogen"	# player starts with a broken bow in inventory
item small NOWHERE	bow2	"Bogen"		"reparierter Bogen"	# script code can later replace it with this one!
item large start	hippo	"Nilpferd"	"ein Nilpferd"		# put a hippo into start location
item small start	umlauts	"äöüßÄÖÜ"	"Umlaute"
# There is a pre-defined pseudo item called "PLAYER". This is invisible to the player, but can
# be moved around by the script (to move the player).

# "asm" passes the remainder of the line to the assembler backend unchanged:
asm HINZ	= color_YELLOW	# puts "HINZ = color_YELLOW" into output file
asm KUNZ	= color_LRED
# ONLY USE THIS FOR SYMBOL DEFINITIONS, NOT FOR ACTUAL MACHINE CODE!

/* (comment out the following docs)

# the remainder of the description file consists of code sequences in the actual
# script language:

loc location_name
#	defines a location in the game. the code sequence is executed whenever
#	the player enters that location.
#	one location MUST be called "start", this is where the game begins.
using itemA itemB
#	defines what happens if the player uses two items together. the code
#	sequence is executed whenever the player enters "use X with Y" and has
#	access to both items.
defproc proc_name
#	starts a procedure definition. the named procedure can then be
#	called from other code sequences.
# a code sequence ends where the next one begins, or at end-of-file.

# "instructions" of the actual script language:
"This is some text", petscii_REVSON, "!", petscii_REVSOFF, cr
#	lines beginning with single or double quotes are text to output.
#	You can use predefined petscii codes like petscii_CLEAR or petscii_REVSON,
#	but do NOT use petscii codes for colors! Use "color_WHITE" etc. instead.
#	"cr" adds a carriage return.
#	Do NOT add null terminators! the converter will do that by itself.
n some_location
s other_location
#	"nsewud" characters indicate target locations when player attempts
#	to go north/south/east/west/up/down from current location.
s NOWHERE
#	you can use the pre-defined pseudo location "NOWHERE" as target to
#	explicitly disable a direction at runtime.
n2 some_location
#	as a convenience function, you can add a "2" to the direction command
#	to enforce a two-way connection:
#	this example line says "going north leads to "some_location",
#	and going south from there leads back here again!
callproc proc_name
#	calls the named procedure
callasm player_has_won
#	this adds code to call a machine language sub-routine. the argument is
#	an assembler label you must define yourself in the surrounding asm code.
delay 5
#	waits a short time. unit is .1 seconds, so 5 would be half a second.
#	wait times of more than a few seconds will not work (because of
#	internal overflow), but those shouldn't be put in a game anyway. :)
dec some_var
#	decrement game variable (subtract 1)
inc other_var
#	increment game variable (add 1)
some_var = other_var_or_literal
#	assign value (in this case, the line's "keyword" is the '=' character)

if some_var == some_value
#	start conditional block
#	possible comparisons: "==", "!=", "<", ">", "<=", ">=", "@", "!@"
#	"@" and "!@" are special operators for "item at location" and
#	"item not at location" check. Instead of a location, another
#	item can be given, then this checks if both items' location
#	are equal / not equal.
elif some_var == other_value
#	any number of "else if" blocks
else
#	optional "else" block
endif
#	end of if/elif/else structure

move some_item some_location
#	move an item to a different location
#	use special location NOWHERE to hide item
#	use special location INVENTORY to put item into player's inventory
# alternative:
move some_item some_other_item
#	move an item to the same location where the other item is
#	use special item PLAYER to move item to current location

*/ (end of comment)

# "using" defines what happens if player tries to "use item X with item Y" (and has access to both):
using bow1 string
	move bow1 NOWHERE	# broken bow disappears
	move bow2 INVENTORY	# repaired bow appears
	"Der Bogen ist nun funktionsbereit!"

using bow2 hippo
	move hippo NOWHERE
	"Der Pfeil geht durch das Nilpferd hindurch, welches sich in Luft auflöst."

# "loc" starts a new location description:
loc deck4_transporter_room
	"You are in what looks like a transporter room right out of ", color_WHITE, "Star Trek", color_GREEN, ".", cr
	"There is a corridor to the north, a turbolift to the east, and an opening to a vertical Jefferies tube."
	"To output double quotes, put them in single quotes as a separate character, like this:", '"', cr
	"", petscii_REVSON, "<= if you want a line to start with a control code, put an empty string before it.", cr
	n corridor_transp_room	# going north leads to the "corridor outside the transporter room" stuation
	e turbolift		# going east leads to the turbolift location
	u deck3_jefferies	# going up leads to "jefferies tube on deck 3" location
	d deck5_jefferies	# going down leads to "jefferies tube on deck 5" location
	# ...now the game will display north/east/up/down as possible directions,
	# but neither south nor west.

	#FIXME - add shorthand command for "alternative action leading to new location"?
	# 'a' is for alternative actions, with key, text and result as arguments
	# remember "nsewud" cannot be used ("nsowhr" if german), so better use digits!

# "defproc" starts a procedure definition (can be called using "callproc")
defproc check_lives
	if lives_left == 0
		"You are so dead."
		delay 10	# wait a full second
		callasm xor_border
	endif


# example:

# 'loc' starts a new location, arg is name
loc start	# <= one location MUST be called "start", this is where the game begins
	"Hi! Hit the correct key to begin the game.", cr
	#a corridor2		FIXME - implement "a"!
	d corridor2
	callproc check_lives

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
	if hippo @ PLAYER
		"You see a hippo."
	elif hippo @ corridor3
		"You can hear a hippo outside the door."
	endif
	n2 corridor3

	# still to do:
	# "restart" to set vars to default?
#

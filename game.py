#!/bin/cat
# this is no python source, the file is only
# called *.py to have syntax coloring!

# see "example.py" for help about the command syntax in this file.

# symbolic constants:
define FALSE	0
define TRUE	1

# variables and default values:

## angesammelte Punkte
var score	0
## Wie weit ist der Zaubertrank fertig 1-8
## Bei Wert 8 ist Zaubertrank getrunken und aktiv
var potion	0
# Wurde der Sarg schon genutzt?
var coffin_used	FALSE
# Wurde die Mistel abgeschnitten?
var mistle_cut	FALSE
# Wurde die Truhe aufgeschlossen?
var chest_opened	FALSE

# "asm" passes the remainder of the line to the assembler backend unchanged:
# ONLY USE THIS FOR SYMBOL DEFINITIONS, NOT FOR ACTUAL MACHINE CODE!
# these five _must_ be defined, they tell the engine which colors to use:
asm color_background	= color_BLACK	# background color
asm color_border	= color_BLACK	# border color
asm color_std		= color_GREEN	# standard text color
asm color_emph		= color_LGREEN	# "emphasized" text color
asm color_out		= color_GRAY1	# "disabled" text color
# this one _must_ be defined, it tells the engine what umlaut encoding to expect:
#	set UTF8 to 0 if _this_ file uses ISO 8859-1 encoding
#	set UTF8 to 1 if _this_ file uses UTF-8 encoding
asm UTF8	= 0

# these two can be used for "special effects":	TODO
asm color_speech	= color_CYAN
asm color_magic		= color_WHITE
# these two could be used to color NPC speech:
asm HINZ	= color_YELLOW	# puts "HINZ = color_YELLOW" into output file
asm KUNZ	= color_LRED

# items:
# (args are size, location, skript name, game name)
#	(must be followed by script code to output description)

## B�cher in der Bibliothek
item small library book1 "Ein gro�es Buch"
	'"', "DAS IST DOCH NUR EINE SICHERUNGSKOPIE!",cr
	"...und andere Ausreden", '"'
item small NOWHERE book2 "Ein kleines Buch"
	'"', "ER WAR DOCH NICHT SEIN VATER!",cr
	"Die gr��te L�ge der Filmgeschichte", '"'
item small NOWHERE book3 "Ein interessantes Buch"
	'"', "BESTIARUM MYSTERICA II", '"', cr
	"Kalahuii sollen laut diesem Fachbuch nur mit Waffengewalt zu besiegen "
	"sein. Aber man sollte daf�r ganz sch�n kr�ftig sein..."
item small NOWHERE book4 "Ein altes Buch"
	'"', "TITANIK II - Sie ist wieder da!", '"', cr
	"Du bl�tterst vor und liest gleich das Ende.", cr
	"Na toll. Sie geht wieder unter."
item small NOWHERE book5 "Ein braunes Buch"
	'"', "TT64",cr
	" Wahnsinnig toll oder nur Wahnsinnig?", '"'
item small NOWHERE book6 "Ein uraltes Buch"
	'"', "KRISTALLOGRAPHIE (c) by Sheltem", '"', cr
	"Die Schwarte handelt von magischen Kristallen. Sollen irgendwie gut "
	"gegen Untote sein, steht hier..."
item small NOWHERE book7 "Ein vergilbtes Buch"
	'"', "HAT SCHON JEMAND CHOPLIFTER GESAGT?", '"', cr
	"Komisches Buch... Egal, unwichtig."
item small NOWHERE book8 "Ein gr�nes Buch"
	'"', "VERPOLTE NETZTEILE UND ANDERE �RGERNISSE", '"', cr
	"Hmm... da steht irgendetwas von geplatzten Kondensatoren...",cr
	"Uninteressant."
item small NOWHERE book9 "Ein winziges Buch"
	'"', "REZEPT F�R ST�RKETRANK", '"', cr
	'"', "Eine Mistel, ein Sumpfkraut, Haare eines Toten, eine frische "
	"Alraune, SCUMM und etwas ranziges Eulenfett, sowie eine Rabenfeder.", '"', cr
	"Dann braucht es noch etwas total unwichtiges, das ebenfalls in den "
	"Kessel geworfen werden muss.",cr
	'"', "Lasse zuletzt deine Magie auf das Gebr�u einwirken!", '"'
item small NOWHERE book10 "Ein schwarzes Buch"
	'"', "ARCANA MAGICA III", '"', cr
	" Das ultimative Nachschlagewerk"
item small NOWHERE book11 "Ein bl�uliches Buch"
	'"', "DURCHK�MMT DIE W�STE!", cr
	" ...und andere Missverst�ndnisse", '"'
item small NOWHERE book12 "Ein Buch mit Runen"
	"Hmm... Ein alchemistischer Prozess um magische Runen zu "
	"kristallifizieren..."
item small NOWHERE book13 "Ein winziges Buch"
	'"', "DER KOPIERSCHUTZ VON ELITE",cr
	" und andere Verbrechen", '"'
item small NOWHERE book14 "Ein unscheinbares Buch"
	'"', "BESTIARUM MYSTERICA I", '"', cr
	"Hmm... Laut diesem Buch sollen Palawaume angeblich immun gegen "
	"Magieschaden sein..."
## Inventar beim Spielstart
item small INVENTORY sickle "Eine goldene Sichel"
	"Mit dieser magischen Sichel kann man hervorragend Misteln schneiden."
item small INVENTORY wand "Ein Zauberstab"
	"Dieser magische Zauberstab ist dein wichtigster Besitz."
## Kr�uter im Garten, braucht erst Sichel oder Spaten
item large garden marten "Ein toter Marder"
	"Hier liegt ein toter Marder.",cr
	" Das stinkende Ding wirst du auf keinen Fall anfassen!"
item large garden tree "Ein gro�er Baum"
	"Ein einzelner Baum steht hier im Garten."
	if mistle_cut == FALSE
		"", cr
		"Ein kleine, gr�nliche Mistel w�chst an einem seiner �ste. Sie "
		"kann von dir abgeschnitten werden."
	endif
item large garden herb "Ein B�schel Sumpfkraut"
	"Etwas Sumpfgras von allerfeinster Qualit�t.",cr
	" Du kannst es abschneiden."
item large NOWHERE alraun "Eine Alraune"
	"Eine ganz normale Alraune, sie scheint noch recht frisch zu sein.",cr
	"Sie steckt fest in der Erde und muss erst ausgegraben werden."
## Nach dem schneiden kann man sie auch nehmen
item small NOWHERE mistle "Eine kleine Mistel"
	"Ein kleiner, gr�nlicher Mistelzweig."
item small NOWHERE herb2 "Ein B�schel Sumpfkraut"
	"Etwas Sumpfgras von allerfeinster Qualit�t."
item small NOWHERE alraun2 "Eine Alraune"
	"Eine ganz normale Alraune, sie scheint noch recht frisch zu sein."
## NPC
item large tomb ghoul "Ein ekeliger Ghoul"
	"Igitt, ist das ein madiges Kerlchen! Der ist ja schon total verwest "
	"und verfault."
item large bedroom pala "Ein echter Palawaum"
	"Wow! Ein krasser Palawaum!"
item large bedroom kala "Ein toller Kalahuii"
	"Boah ey! Voll geil, ein Kalahuii!"
item large observatory raven "Ein schwarzer Rabe"
	"Ein majest�tischer Rabe, mit pechschwarzem, leicht bl�ulich schimmernden "
	"Gefieder. Klug blickt er Dich aus seinen kleinen Augen an. Eine erhabene "
	"magische Aura scheint ihn zu umgeben."
## Nicht verwendet
item large NOWHERE flonk "Ein lebendiger Flonk"
	"Wie niedlich, ein Flonk!"
## Nur f�r Bonuspunkt
item small kitchen burger "Ein Hamburger"
	"Lecker, mit K�se und Speck!",cr
	" Scheint ein Mac Bacon zu sein."
## Hilfsmittel
item small NOWHERE sword "Ein Schwert"
	"Bei dieser Waffe handelt es sich um das magische Schwert 'Thunderblade'."
item small NOWHERE crystal "Ein Kristall"
	"Dieser magische Kristall soll angeblich Untote bannen k�nnen."
item small NOWHERE spade "Ein rostiger Spaten"
	"Ein ganz normaler, alter Spaten."
item small NOWHERE rune "Eine Rune"
	"Diese Rune strahlt geradezu vor magischer Energie."
item small NOWHERE jemmy "Ein Brecheisen"
	"Ein schwerer Kuhfu� aus Stahl."
item small kitchen cheese "Ein kleines St�ck K�se"
	"Boah, stinkt der!!!",cr
	"Muss wohl ein Oobdool�nder oder was anderes kurioses sein.",cr
	"Essen wirst du diesen Sonderm�ll jedenfalls nicht. Sowas schmeckt "
	"Dir nicht."
item small tomb key "Ein Schl�ssel"
	"Ein ziemlich altes, rostiges Ding."
## Zauberzutaten (Ohne die Gartenkr�uter)
item small laboratory fat "Etwas Eulenfett"
	"Fein abgetriebenes, ranziges Eulenfett."
item small NOWHERE feath "Eine Feder"
	"Eine schwarze Rabenfeder."
item small NOWHERE hair "Ein B�schel Haare"
	"Die Haare eines toten Menschen..."
item small observatory scumm "Etwas SCUMM"
	"Erstklassiges SCUMM. Damit kann man sicher tolle Sachen machen."
item small bathroom hering "Ein Hering"
	"Ein roter Hering?",cr
	"Sieht ja enorm wichtig aus...",cr
	"Aber sicher zu nichts zu gebrauchen."
## Einrichtung
item large kitchen kettle "Ein gro�er Kessel"
	"Ein riesiger Hexenkessel aus Gu�eisen."
item large tomb coffin "Ein schwerer Sarg"
	"Ein gro�er Sarg, der aus einem St�ck Stein gemei�elt worden zu sein "
	"scheint."
item large laboratory chem "Lauter alchemistisches Ger�mpel"
	"Gl�ser und Flaschen und Kolben und Phiolen und Becher und R�hrchen..."
item large library shelf "Drei B�cherregale"
	"Die hohen Regale an den W�nden bedecken alle W�nde und nehmen den "
	"Gro�teil des Raumes ein.",cr
	"Sie sind rappelvoll mit dicken Schwarten."
item large study chest "Eine Truhe"
	"Ein schwere, eisenbeschlagene Truhe aus Eichholz.",cr
	if chest_opened == FALSE
		"Was da wohl drin sein mag?"
	else
		"Sie ist ge�ffnet und leer."
	endif

# usages:

## Die B�cher im Regal
proc bookswap
	"Die Regale sind gestopft voll. Also nimmst du erst ein neues Buch "
	"heraus und steckst das alte dann in die freie L�cke.", cr
	"Buch gegen Buch, toller Tausch."
using shelf book1
	hide book1
	gain book2
	callproc bookswap
using shelf book2
	hide book2
	gain book3
	callproc bookswap
using shelf book3
	hide book3
	gain book4
	callproc bookswap
using shelf book4
	hide book4
	gain book5
	callproc bookswap
using shelf book5
	hide book5
	gain book6
	callproc bookswap
using shelf book6
	hide book6
	gain book7
	callproc bookswap
using shelf book7
	hide book7
	gain book8
	callproc bookswap
using shelf book8
	hide book8
	gain book9
	callproc bookswap
using shelf book9
	hide book9
	gain book10
	callproc bookswap
using shelf book10
	hide book10
	gain book11
	callproc bookswap
using shelf book11
	hide book11
	gain book12
	callproc bookswap
using shelf book12
	hide book12
	gain book13
	callproc bookswap
using shelf book13
	hide book13
	gain book14
	callproc bookswap
using shelf book14
	hide book14
	gain book1
	callproc bookswap

## Die Sachen im Garten
proc find_alraune
	"An der Stelle wo der Kadaver lag, kann man eine Alraune in der Erde "
	"erkennen."
using spade marten
	hide marten
	move alraun garden
	inc score
	"Du schaufelst den Kadaver auf den Spaten und schleuderst das "
	"stinkende Ding ins Moor.",cr
	callproc find_alraune
using wand marten
	hide marten
	move alraun garden
	inc score
	"Du klatscht dem Kadaver einen Zauberspruch vor den Latz!",cr,cr
	delay 5
	"", color_speech, '"', "SIMSALAKADABRA-ABRAKABUM!", '"', color_std, cr
	delay 5
	"", color_magic, "ZISCH, PUFF, PENG!", color_std, cr
	delay 5
	"Weg ist das stinkende Ding.",cr
	callproc find_alraune
using spade alraun
	hide alraun
	inc score
	gain alraun2
	"Du buddelst die Alraune mit dem Spaten aus und steckst sie gleich "
	"ein.",cr
	"Alraunen kann ein Zauberer schlie�lich immer gebrauchen."

using sickle herb
	hide herb
	inc score
	move herb2 garden
	"Du erntest das Sumpfkraut mit deiner goldenen Sichel.",cr
	"Jetzt kannst du es einfach einsammeln."
using sickle tree
	if mistle_cut == FALSE
		mistle_cut = TRUE	# Damit man nur einmal Misteln holen kann
		inc score
		move mistle garden
		"Du erntest die Mistel mit deiner goldenen Sichel.",cr
		"Jetzt kannst du sie einfach einsammeln."
	else
		"Was willst du denn da noch abschneiden?"
	endif
using jemmy coffin
	if coffin_used == FALSE
		coffin_used = TRUE # Damit man nur einmal Haare holen kann
		inc score
		gain hair
		"Du �ffnest den Sarg mit dem Kuhfu�.",cr
		"Dein Gro�vater reicht dir ein B�schel seiner Haare. Du "
		"bedankst dich und schlie�t den Sarg wieder."
	else
		"Du willst gerade wieder das Brecheisen am Sargdeckel "
		"ansetzen, entsinnst dich dann aber doch anders und l�sst "
		"deiner toten Verwandtschaft ihre Ruhe.",cr
		"Mehr als ein Haarb�schel brauchst du ja nicht."
	endif
using rune chem
	hide rune
	inc score
	gain crystal
	"Du wendest das alchemistische Verfahren auf die Rune an und erh�ltst "
	"nach kurzer Zeit einen h�bschen Kristall."
using cheese raven
	hide cheese
	hide raven
	inc score
	gain feath
	"Der Rabe macht sich gierig �ber den K�se her.",cr
	"Blitzschnell greifst du zu, und rupfst ihm eine Feder aus.",cr
	"Na wer sagts denn, das verfressene Vogeltier hat es gar nicht "
	"mitbekommen."
## Die K�mpfe
using sword pala
	if  potion == 9
		hide pala
		inc score
		move rune bedroom
		"Ja, mit dem Schwert und genug Schmalz in den Oberarmen kann "
		"man einen Palawaum besiegen!", cr, cr
		delay 2
		"Du hackst das dumme, magieresistente Ding in St�cke!", cr, cr
		"Aus der Leiche f�llt eine Rune."
	else
		"Du bist viel zu schwach, du H�nfling!", cr
		"Iss erstmal dein M�sli auf!"
	endif
using wand kala
	hide kala
	inc score
	move spade bedroom
	"Na also, mit Magie kann man so einen Kalahuii besiegen!",cr,cr
	delay 2
	"Du pulverisierst das d�mliche, gegen physischen Schaden gefeite "
	"Mistding!",cr,cr
	"Aus der Leiche f�llt ein alter Spaten."
using crystal ghoul
	hide ghoul
	inc score
	"Jawoll, das haut ja prima hin!",cr
	"Die magischen Kr�fte des Kristalls blasen dem ollen Ghoul sein "
	"untotes Dasein aus!", cr, cr
	delay 2
	"Der Bursche zerf�llt zu Staub!",cr,cr
	delay 2
	"DU HAST DAS ADVENTURE GEL�ST!"
	#delay 10
	#callasm get_key
	#callasm restart
# Das Zubereiten des Zaubertrankes
# Wenn Variable potion auf 9 steht, ist der Trank aktiv
using kettle herb2
	hide herb2
	inc potion
	inc score
	"Du wirfst das Sumpfkraut in den Kessel."
using kettle alraun2
	hide alraun2
	inc potion
	inc score
	"Du wirfst die Alraune in den Kessel."
using kettle mistle
	hide mistle
	inc potion
	inc score
	"Du wirfst die Mistel in den Kessel."
using kettle scumm
	hide scumm
	inc potion
	inc score
	"Du wirfst SCUMM in den Kessel."
using kettle hair
	hide hair
	inc potion
	inc score
	"Du wirfst das B�schel Haare in den Kessel."
using kettle fat
	hide fat
	inc potion
	inc score
	"Du wirfst das Eulenfett in den Kessel."
using kettle feath
	hide feath
	inc potion
	inc score
	"Du wirfst die Rabenfeder in den Kessel."
using kettle hering
	hide hering
	inc potion
	inc score
	"Du wirfst den Hering in den Kessel."
using kettle wand
	if potion == 8
		inc potion
		inc score
		"Du wedelst mit Deinem Zauberstab.",cr
		delay 2
		"Du murmelst magische Formeln.",cr
		delay 2
		"", color_speech, '"', "BRUMMEL, BRUMMEL, BRABBEL, "
		"BRABBEL...", '"', color_std, cr, cr
		delay 2
		"Der Trank ist fertig!",cr
		"Sofort trinkst du ihn aus.",cr,cr
		"WOW! F�hlst du dich jetzt kr�ftig!"
	else
		"Du hast noch nicht alle Zutaten in den Kessel geworfen!",cr
		"Erst wenn die Mischung komplett ist, kannst du deine Magie "
		"wirken lassen."
	endif 
## Bonuspunkt
using key chest
	if chest_opened == FALSE
		chest_opened = TRUE	# Nicht nochmal!
		move sword study
		move jemmy study
		"Du �ffnest die Truhe mit dem Schl�ssel. Sie enth�lt ein "
		"Schwert und ein Brecheisen."
	else
		"Du hast die Kiste bereits ge�ffnet."
	endif
using sword cheese
	"Oh nein, der K�se wird nicht aufgeschnitten!",cr
	"Dann stinkt das ganze Schwert nach dem Zeug!"
using ghoul burger
	hide burger
	inc score
	"Der Ghoul entfernt erst einmal angewidert die Gurkenscheibe. Nicht "
	"einmal ein Untoter mag die.", cr
	"Dann verschlingt er schmatzend den leckeren Hamburger.", cr,cr
	"Das bringt dich aber leider nicht weiter.",cr,cr
	"Vielleicht h�ttest du ihn vorher vergiften sollen?",cr
	"Nee, falsches Spiel...",cr
	"Das war bei ROBOX..."
proc sichel_statt_schwert
	"Man muss Zauberzutaten mit einer goldenen Sichel schneiden!"
using sword herb
	callproc sichel_statt_schwert
using sword mistle
	callproc sichel_statt_schwert
proc wirf_in_kessel
	"Das kannst du hier nicht gebrauchen. Das musst du in einen "
	"Zauberkessel werfen."
using herb2 chem
	callproc wirf_in_kessel
using alraun2 chem
	callproc wirf_in_kessel
using mistle chem
	callproc wirf_in_kessel
using hering chem
	callproc wirf_in_kessel
using feath chem
	callproc wirf_in_kessel
using fat chem
	callproc wirf_in_kessel
using scumm chem
	callproc wirf_in_kessel
using hair chem
	callproc wirf_in_kessel
## K�mpfe die nicht zum Ziel f�hren
using wand pala
	"Der Palawaum ist gegen Magieschaden immun und lacht dich aus!"
using sword kala
	"Der Kalahuii ist gegen physische Sch�den immun und verspottet dich!"
using sword ghoul
	if sword !@ INVENTORY
		"Dazu musst du es erstmal aufheben, Hirni!"
	else
		move sword tomb
		inc score
		"Gelangweilt haut dir der Ghoul dein Schwert aus den H�nden."
	endif
using jemmy pala
	move jemmy garden
	inc score
	"Kichernd schnappt sich das Palawaum deinen Kuhfu� und rennt damit "
	"davon.",cr
	"Blitzschnell ist es wieder da und grinst dich an.",cr
	"Dein Brecheisen hat es anscheinend irgendwo im Turm versteckt..."
using jemmy kala
	"Du haust dem Kalahuii das Brecheisen auf den D�z.",cr
	"Es guckt dich treuherzig an.",cr
	"Das scheint ihm gefallen zu haben."
using jemmy ghoul
	"Der Ghoul blockt deinen Angriff ohne Probleme ab.",cr
	"Mit so einer Waffe kommt man dem Kerl nicht bei..."
using wand ghoul
	"Der Ghoul guckt dich nur dumm an.",cr,cr
	"Deine �blichen Zauberspr�che scheinen bei dem gar nichts zu bringen."
using sword raven
	"Der Rabe flattert dir davon, als er Dich mit dem Schwert ankommen "
	"sieht. Der scheint clever zu sein."
using jemmy raven
	"Der Rabe flattert vor dir davon, als er Dich mit dem Brecheisen "
	"sieht.",cr
	"Der will wohl nicht gekeult werden. Irgendwie auch verst�ndlich..."
using wand raven
	"Du fuchtelst mit deinem Zauberstab.",cr
	delay 3
	"", color_magic, "ZACK!", color_std, cr,cr
	delay 3
	"Der Vogel scheint etwas Besonderes zu sein. Er hat einen Blitz nach "
	"dir geworfen!",cr
	delay 2
	"Scheint eine Art von Thunderbird zu sein...",cr
	delay 2
	"So klappt das nicht."
using spade pala
	"Mit einem Spaten?",cr
	"Besorg dir eine bessere Waffe!"
using spade ghoul
	"Der Ghoul schmei�t sich weg vor Lachen, als du unbeholfen mit dem "
	"Spaten auf ihn einschlagen willst."
using spade raven
	"Der Rabe kr�ht und faucht dich w�tend an, als du mit dem dem Spaten "
	"auf ihn losgehen willst.",cr,cr
	"Erschrocken weichst du einen Schritt zur�ck."
using sickle pala
	"Mit einer Sichel kann man keine Kalahuiis t�ten."
using sickle kala
	"Du haust dem Kalahuii deine Sichel auf die Birne.",cr
	"Sinnlos, das macht ihm gar nichts aus."
using sickle raven
	if sickle !@ INVENTORY
		"Heb deine Sichel erst einmal auf."
	else
		move sickle observatory
		"Der Rabe hackt dir Krallen in den Arm. Erschrocken l�sst du "
		"deine Sichel fallen."
	endif
using sickle ghoul
	"Der Ghoul meckert nur ein wenig, als du versuchst ihn mit deiner "
	"goldenen Sichel anzugreifen.",cr
	"Du h�rst lieber auf, bevor er noch richtig w�tend wird."
## Noch ein paar Versuche was zu zaubern
using wand shelf
	"Du kennst leider keinen Zauberspruch, mit dem sich B�cher sortieren "
	"lassen."
using wand coffin
	if coffin_used == FALSE
		"Du traust dich nicht, an dem Sarg herumzuzaubern. Da liegt "
		"dein Gro�vater drin und du willst ihn nicht w�tend machen.",cr
		"Einen Zauberer sollte man auch dann nicht ver�rgern, wenn "
		"er schon lange tot ist."
	else
		"Du traust dich nicht, an dem Sarg herumzuzaubern. Du hast "
		"deinen Gro�vater heute schon genug gest�rt."
	endif
using wand chem
	"Was willst du denn an deiner Laborausr�stung verzaubern? Da ist "
	"alles so wie es sein soll."
using wand sickle
	"Die Sichel besteht aus Gold und kann nicht verzaubert werden.",cr
	"Jedenfalls nicht von dir, da braucht es schon einen zwergischen "
	"Runenmagier. Die k�nnen sowas angeblich."
using wand sword
	"Das Schwert muss nicht verzaubert werden, das ist schon eine "
	"magische Waffe."
using wand jemmy
	"Ein Brecheisen verzaubern? Auf was f�r Ideen kommst du denn?"

# procedures:
proc intro
	delay 5
	"", color_WHITE, petscii_CLEAR, cr, cr
	#1234567890123456789012345678901234567890
	"                Saufbox!", cr, cr, cr, cr
	delay 10
	"              pr�sentiert:", cr, cr, cr, cr
	delay 5
	"      Adventure of the Bunkerparty", cr
	"                  V1.1", cr, cr, cr
	delay 5
	"     Code:  TheIncredibleBauchspeck", cr
	"     Story:           Clumsy Wizard", cr, cr, cr, cr, cr
	delay 5
	"Bitte eine Taste dr�cken..."
	# "Welcome to Multiple Choice Adventure 2!", cr, cr
	# "Press any key..."
	callasm get_key
	"", color_std, petscii_CLEAR
	"Der Magier Petrosilius hat sich letztens mit dem Gebiet der Nekromantie "
	"befasst und hat seither ein kleines Problem. In seinem Keller haust nun ein "
	"d�mlicher Ghoul, den er nicht mehr los wird. H�tte er das gewusst, w�re er "
	"lieber bei seinen Fachgebieten Elementarismus und Illusionsmagie geblieben, "
	"aber nun ist es zu sp�t.", cr
	"Als ob das nicht schon genug �rger w�re, hat es sein Zaubererfreund Mabruk "
	"auch noch gut mit ihm gemeint. Er versuchte den Ghoul mit einem "
	"Beschw�rungsritual zu vernichten, doch leider laufen seither auch noch ein "
	"Kalahuii und ein Palawaum in Petrosilius Turm herum...", cr
	"Nun... Dann mal auf, mal schauen wie man die ungebetenen G�ste wieder "
	"loswerden kann...", cr
	"Deinen Zauberstab und deine goldene Sichel hast du schon einmal "
	"eingesteckt, diese Sachen wirst du sicher brauchen. Vermutlich "
	"w�re es das Schlaueste, erstmal ein wenig in der Bibliothek zu "
	"recherchieren..."
	callasm get_key

# locations:
loc start
	"Flur im Erdgeschoss",cr
	"Du stehst im Eingangsbereich deines Magierturmes.",cr
	"Im S�den befindet sich die Haust�r, "
	"nach Osten und Westen f�hren Durchg�nge. Im Norden des Raumes f�hrt "
	"eine steinerne Treppe in die oberen "
	"Stockwerke oder hinab in den Keller.",cr
	w2 kitchen
	e2 bathroom
	s2 garden
	d2 tomb
	u2 floor1

loc floor1
	"Flur im ersten Stock",cr
	"Du befindest Dich in einem kleinen "
	"Treppenhaus, in dem sich die steinerne "
	"Treppe sowohl nach oben als nach "
	"unten weiter windet. Es ist hier zwar "
	"weder kalt noch muffig, aber doch "
	"etwas trostlos. Ein schwacher Lichtschimmer dringt aus einem Durchgang im "
	"Osten. Eine T�r aus dunklem Holz f�hrt "
	"nach Westen.",cr
	w2 study
	e2 bedroom
	u2 floor2

loc floor2
	"Flur im zweiten Stock",cr
	"Eng windet sich die Wendeltreppe nach "
	"oben und unten. Du fragst Dich, wann "
	"die Treppe endlich ein Ende hat. Ein "
	"kleiner Nebengang f�hrt nach Westen, "
	"im Osten befindet sich eine h�lzerne "
	"T�re mit Eisenbeschl�gen. Ein kleines "
	"Fenster spendet etwas Licht.",cr
	w2 laboratory
	e2 library
	u2 observatory

loc observatory
	"Observatorium",cr
	"Hier oben im Observatorium deines Turms "
	"hast Du einen gro�artigen Blick �ber "
	"den Zauberwald. Im Westen siehst Du die "
	"ber�hmten Silberberge mit ihren schneebedeckten Gipfeln. Der Ausblick l�sst "
	"Dich den beschwerlichen Aufgang �ber "
	"die Wendeltreppe vergessen. Ein einfacher Tisch mit einem h�lzernen Stuhl "
	"sind neben deinem Teleskop die einzigen "
	"Einrichtungsgegenst�nde hier.",cr

loc tomb
	"Gruft",cr
	"Du bist nun in einem uralten, unterirdischen Grabgew�lbe, der Gruft in der "
	"deine Ahnen ruhen. Zu beiden Seiten "
	"stehen alte Grabsteine, deren Inschriften nicht mehr zu entziffern "
	"sind. Die W�nde bestehen aus gemauertem "
	"Stein, der von Moder �berzogen ist.",cr
	"Eine ideale Umgebung f�r alle "
	"Kreaturen, die das Licht scheuen.",cr
	"Mitten im Raum steht ein schlichter "
	"Altar, an der Nordmauer ist ein Sarg "
	"abgestellt.",cr

loc garden
	"Kr�utergarten", cr
	"Du stehst in einem kleinen, h�bschen Vorgarten. Der Garten ist von einem "
	"kleinen Zaun umgeben. Unmittelbar "
	"dahinter beginnt im S�den das Modermoor, w�hrend der Turm von allen "
	"anderen Seiten vom Salamanderwald "
	"eingeschlossen ist. Neben einem "
	"Blumenbeet siehst Du vor allem "
	"mehrere Kr�uterbeete.",cr
	"Nach Norden kannst du deinen Magierturm betreten.",cr

loc kitchen
	"K�che", cr
	"Hier in der K�che bereitet deine Ehegattin ihre leckeren Sachen zu. Unter "
	"Kennern sind ihre Kochk�nste weit bekannt. Leider ist sie momentan auf "
	"Reisen. Du siehst einen Herd, einen "
	"K�chenschrank, einen Tisch und St�hle. "
	"Neben dem Herd ist eine Sp�le. An "
	"einer Wand h�ngt ein Regal. Im S�den "
	"steht die Schlafpritsche deines "
	"Lehrlings.", cr

loc bathroom
	"Badezimmer", cr
	"Das ist der Baderaum. Eine Dusche steht "
	"in einer Ecke. �ber dem Waschbecken "
	"kannst Du einen Spiegel erkennen. Die "
	"Badematte am Boden ist feucht, wahrscheinlich wurde hier vor kurzem gerade "
	"geduscht. Ein kleiner Schemel und ein "
	"h�lzerner Eimer stehen im Raum.", cr

loc study
	"Wohn- und Studienzimmer", cr
	"Eine Vitrine, ein Regal und ein abschlie�bares Schr�nkchen h�ngen hier "
	"in deinem Wohnzimmer an den W�nden. "
	"Ein magischer Schreibtisch, der aussieht, als ob er aus einem riesigen "
	"Tigerauge gefertigt wurde, befindet "
	"sich in der Mitte des Raumes. Dann "
	"steht da noch ein bequemer Sessel "
	"beim Kamin an der Westwand. Ein "
	"Durchgang f�hrt zur�ck nach Osten.", cr

loc bedroom
	"Schlafzimmer",cr
	"Das Schlafzimmer ist recht spartanisch "
	"eingerichtet. An der S�dwand steht ein "
	"gro�es Bett, an der Ostwand ein riesiger Schrank. Rund um das Bett ist "
	"ein L�ufer ausgelegt und neben dem Bett "
	"steht ein kleines Nachtschr�nkchen. "
	"Eine T�r aus schwerem Holz f�hrt im "
	"Westen zur�ck ins Treppenhaus.",cr

loc laboratory
	"Alchemie-Labor", cr
	"Du bist in einem Turmzimmer gelandet, "
	"das �ber und �ber mit merkw�rdigen "
	"Apparaten gef�llt ist. Da brodelt, "
	"funkt und zischt es, dass es eine reine "
	"Freude ist. Nat�rlich wei� ein Fachmann wie du genauestens Bescheid, wozu "
	"die Apparate dienen, die auf dem Tisch "
	"stehen. In manchen brodeln Dir wohlbekannte Chemikalien vor sich hin. Sie "
	"sehen wundersch�n giftig aus. Nach "
	"Osten kannst du den Raum durch eine "
	"T�r verlassen.",cr

loc library
	"Bibliothek", cr
	"An s�mtlichen W�nden des Raumes stehen "
	"Regale bis unter die Decke, und alle "
	"Regale sind mit B�chern und anderen "
	"Schriftst�cken vollgestopft. Wie soll "
	"ein zerstreuter Zauberer hier bloss "
	"finden, wonach er sucht?",cr
	"Ohne Bibliothekar erscheint Dir das "
	"beinahe aussichtslos.", cr

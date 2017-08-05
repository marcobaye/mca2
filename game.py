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

#
# items:
# (args are size, location, skriptname, shortdesc, longdesc)

## B�cher in der Bibliothek
item small library book1 "Ein grosses Buch" "DAS IST DOCH NUR EINE SICHERUNGSKOPIE!",cr," ...und andere Ausreden"
item small NOWHERE book2 "Ein kleines Buch" "ER WAR DOCH NICHT SEIN VATER!",cr," Die gr�sste L�ge der Filmgeschichte"
item small NOWHERE book3 "Ein interessantes Buch" "Kalahuii sollen laut diesem Fach-",cr," buch nur mit Waffengewalt zu besiegen",cr," sein. Aber man sollte daf�r ganz",cr," sch�n kr�ftig sein..."
item small NOWHERE book4 "Ein altes Buch" "TITANIK II - Sie ist wieder da!"
item small NOWHERE book5 "Ein braunes Buch" "TT64",cr," Wahnsinnig toll oder nur Wahnsinnig?"
item small NOWHERE book6 "Ein uraltes Buch" "Die Schwarte handelt von magischen",cr," Kristallen.",cr,"Sollen irgendwie gut gegen Untote",cr,"sein, steht hier..."
item small NOWHERE book7 "Ein vergilbtes Buch" "HAT SCHON JEMAND CHOPLIFTER GESAGT?"
item small NOWHERE book8 "Ein gr�nes Buch" "VERPOLTE NETZTEILE UND ANDERE �RGERNISSE"
item small NOWHERE book9 "Ein winziges Buch" "REZEPT F�R ST�RKETRANK",cr," Eine Mistel, ein Sumpfkraut,",cr," Haare eines Toten, eine fische",cr," Alraune, SCUMM und etwas ranziges",cr," Eulenfett, sowie eine Rabenfeder.",cr," Zuletzt muss noch etwas total un-",cr," wichtiges in den Kessel geworfen",cr," werden."
item small NOWHERE book10 "Ein schwarzes Buch" "ARCANA MAGICA III",cr," Das ultimative Nachschlagewerk"
item small NOWHERE book11 "Ein bl�uliches Buch" "DURCHK�MMT DIE W�STE!",cr," ...und andere Missverst�ndisse"
item small NOWHERE book12 "Ein Buch mit Runen" "Hmm... Ein alchmestischer Prozess um",cr," magische Runen zu kristallifizieren.."
item small NOWHERE book13 "Ein winziges Buch" "DER KOPIERSCHUTZ VON ELITE",cr," und andere Verbrechen"
item small NOWHERE book14 "Ein unscheinbares Buch" "Hmm... Laut diesem Buch sollen Pala-",cr," waums angeblich imun gegen Magie-",cr," schaden sein..."
## Inventar beim Spielstart
item small INVENTORY sickle "Eine goldene Sichel" "Mit dieser magischen Sichel kann",cr," man hervorragend Misteln schneiden."
item small INVENTORY wand "Eine Zauberstab" "Dieser magische Zauberstab ist",cr," dein wichtigster Besitz."
## Kr�uter im Garten, braucht erst Sichel oder Spaten
item large garden marten "Ein toter Marder" "Hier liegt ein toter Marder.",cr," Das stinkende Ding wirst",cr," du auf keinen Fall anfassen!"
item large garden mistle "Eine kleine Mistel" "Ein kleiner, gr�nlicher Mistelzweig",cr," w�chst hier und kann von dir ab-",cr," geschnitten werden."
item large garden herb "Ein B�schel Sumpfkraut" "Etwas Sumpfgras von allerfeinster",cr," Qualit�t.",cr," Du kannst es abschneiden."
item large NOWHERE alraun "Eine Alraune" "eine ganz normale Alraune, sie",cr," scheint noch recht frisch zu sein.",cr," Sie steckt fest in der Erde und",cr," muss erst ausgegraben werden."
## Nach dem schneiden kann man sie auch nehmen
item small NOWHERE mistle2 "Eine kleine Mistel" "Ein kleiner, gr�nlicher Mistelzweig."
item small NOWHERE herb2 "Ein B�schel Sumpfkraut" "Etwas Sumpfgras von allerfeinster",cr," Qualit�t."
item small NOWHERE alraun2 "Eine Alraune" " eine ganz normale Alraune, scheint",cr," noch recht frisch zu sein."
## NPC
item large tomb ghoul "Ein ekeliger Ghoul" "Igitt, ist das ein madiges",cr," Kerlchen! Der ist ja schon total",cr," verwest und verfault."
item large bedroom pala "Ein echter Palawaum" "Wow! Ein krasser Palawaum!"
item large bedroom kala "Ein toller Kalahuii" "Boah ey! Voll geil, ein Kalahuii!"
item large observatory raven "Ein schwarzer Rabe" "Ein majest�tischer Rabe, mit pech-",cr," schwarzem, leicht bl�ulich schim-",cr," mernden Gefieder. Klug blickt er Dich",cr," aus seinen kleinen Augen an. Eine",cr," erhabene magische Aura scheint ihn",cr," zu umgeben."
## Nicht verwendet
item large NOWHERE flonk "Ein lebendiger Flonk" "Wie niedlich, ein Flonk!"
## Nur f�r Bonuspunkt
item small kitchen burger "Ein Hamburger" "Lecker, mit K�se und Speck!",cr," Scheint ein Mac Bacon zu sein."
## Hilfsmittel
item small study sword "Ein Schwert" "Bei dieser Waffe handelt es sich",cr," um das magische Schwert 'Thunderblade'."
item small NOWHERE crystal "Ein Kristall" " Dieser magische Kristall soll",cr," angeblich Untote bannen k�nnen."
item small NOWHERE spade "Ein rostiger Spaten" "Ein ganz normaler, alter Spaten."
item small NOWHERE rune "Eine Rune" "Diese Rune strahlt geradezu vor",cr," magischer Energie."
item small study jemmy "Ein Brecheisen" "Ein schwerer Kuhfuss aus Stahl."
item small kitchen cheese "Ein kleines St�ck K�se" "Boah, stinkt der!!!",cr," Muss wohl ein Oobdool�nder",cr," oder was anderes kurioses sein.",cr," Essen wirst du diesen Sonder-",cr," m�ll jedenfalls nicht. Sowas schmeckt",cr," Dir nicht."
## Zauberzutaten (Ohne die Gartenkr�uter)
item small laboratory fat "Etwas Eulenfett" "Fein abgetriebenes, ranziges Eulenfett."
item small NOWHERE feath "Eine Feder" "Eine schwarze Rabenfeder."
item small NOWHERE hair "Ein B�schel Haare" "Die Haare eines toten Menschen..."
item small observatory scumm "Etwas SCUMM" "Erstklassiges SCUMM. Damit kann man",cr," sicher tolle Sachen machen."
item small bathroom hering "Ein Hering" "Ein roter Hering?",cr," Sieht ja enorm wichtig aus...",cr," Aber sicher zu nichts zu gebrauchen."
## Einrichtung
item large kitchen kettle "Ein grosser Kessel" "Ein riesiger Hexenkessel aus Gu�eisen."
item large tomb coffin "Ein schwerer Sarg" "Ein gro�er Sarg, der aus einem St�ck",cr," Stein gemeisselt worden zu scheint."
item large NOWHERE coffin2 "Ein schwerer Sarg" " Ein gro�er Sarg, der aus einem St�ck",cr," Stein gemeisselt worden zu scheint."
item large laboratory chem "Lauter alchemistisches Ger�mpel" "Gl�ser und Flaschen und Kolben und",cr," Phiolen und Becher und R�hrchen..."
item large library shelf "Ein B�cherregal" "Das B�cheregal geht ums Eck und",cr," nimmt fast den ganzen Raum ein.",cr," Es ist rappelvoll mit dicken Schwarten."


# "asm" passes the remainder of the line to the assembler backend unchanged:
# these two are used for colored text output
asm HINZ	= color_YELLOW	# puts "HINZ = color_YELLOW" into output file
asm KUNZ	= color_LRED

# ONLY USE THIS FOR SYMBOL DEFINITIONS, NOT FOR ACTUAL MACHINE CODE!
# usages:

## Die B�cher im Regal
using shelf book1
	hide book1
	gain book2
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book2
	hide book2
	gain book3
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book3
	hide book3
	gain book4
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book4
	hide book4
	gain book5
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book5
	hide book5
	gain book6
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book6
	hide book6
	gain book7
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book7
	hide book7
	gain book8
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book8
	hide book8
	gain book9
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book9
	hide book10
	gain book10
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book10
	hide book10
	gain book11
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book11
	hide book11
	gain book12
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book12
	hide book12
	gain book13
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book13
	hide book13
	gain book14
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."
using shelf book14
	hide book14
	gain book1
	"Das Regal ist gestopft voll.",cr,"Also nimmst du erst ein neues Buch",cr,"heraus und steckst das alte dann",cr,"in die freie L�cke.",cr,"Buch gegen Buch, toller Tausch."

## Die Sachen im Garten
using spade marten
	hide marten
	move alraun garden
	inc score
	"Du schaufelst den Kadaver auf den",cr,"Spaten und schleuderst das",cr,"stinkende Ding ins Moor.",cr,"An der Stelle wo der Kadaver",cr,"lag, kann man eine Alraune",cr,"in der Erde erkennen."
using wand marten
	hide marten
	move alraun garden
	inc score
	"Du klatscht dem Kadaver einen",cr,"Zauberspruch vor den Latz!",cr,cr,"SIMSALAKADABRA-ABRAKABUM!",cr,"ZISCH, PUFF, PENG!",cr,"Weg ist das stinkende Ding.",cr,"An der Stelle wo der Kadaver",cr,"lag, kann man eine Alraune",cr,"in der Erde erkennen."
using spade alraun
	hide alraun
	inc score
	gain alraun2
	"Du buddelst die Alraune mit dem Spaten",cr,"aus und steckst sie gleich ein.",cr,"Alraunen kann ein Zauberer schlie�lich",cr,"immer gebrauchen."

using sickle herb
	hide herb
	inc score
	move herb2 garden
	"Du erntest das Sumpfkraut mit deiner",cr,"goldenen Sichel.",cr,"Jetzt kannst du es einfach einsammeln."
using sickle mistle
	hide mistle
	inc score
	move mistle2 garden
	"Du erntest die Mistel mit deiner",cr,"goldenen Sichel.",cr,"Jetzt kannst du sie einfach einsammeln."
using jemmy coffin
	inc score
	gain hair
	hide coffin
	move coffin2 tomb # Damit man nur einmal Haare holen kann
	"Du �ffnest den Sarg mit dem Kuhfuss.",cr,"Dein Gro�vater reicht dir ein B�schel",cr,"seiner Haare. Du bedankst dich und",cr,"schliesst den Sarg wieder."
using rune chem
	hide rune
	inc score
	gain crystal
	"Du wendest das alchemistische Ver-",cr,"fahren auf die Rune an und erh�ltst",cr,"nach kurzer Zeit einen h�bschen",cr,"Kristall."
using cheese raven
	hide cheese
	hide raven
	inc score
	gain feath
	"Der Rabe macht sich gierig �ber den",cr,"K�se her.",cr,"Blitzschnell greifst du zu, und",cr,"rupfst ihm eine Feder aus.",cr,"Na wer sagts denn, das verfressene",cr,"Vogeltier hat es gar nicht mitbekommen."
## Die K�mpfe
using sword pala
if  potion == 8
	hide pala
	inc score
	move rune bedroom
	"Ja, mit dem Schwert kann man einen",cr,"Palawaum besiegen!",cr,cr,"Du hackst das dumme, magieresistente",cr,"Ding in St�cke!",cr,cr,"Aus der Leiche f�llt eine Rune."
	else
	"Du bist viel zu schwach, du H�nfling!"
	endif
using wand kala
	hide kala
	inc score
	move spade bedroom
	"Na also, mit Magie kann man so einen",cr,"Kalawuii besiegen!",cr,cr,"Du pulverisierst das d�mliche,",cr,"gegen physischen Schaden gefeite",cr,"Mistding!",cr,cr,"Aus der Leiche f�llt ein alter Spaten."
using crystal ghoul
	hide ghoul
	inc score
	"Jawoll, das haut ja prima hin!",cr,"Die magischen Kr�fte des Kristalls",cr,"blasen dem ollen Ghoul sein untotes",cr,"Dasein aus!",cr,cr,"Der Bursche zerf�llt zu Staub!",cr,cr,"DU HAST DAS ADVENTURE GEL�ST!"
# Das Zubereiten des Zaubertrankes
# Wenn Variable potion auf 8 steht, ist der Trank aktiv
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
using kettle mistle2
	hide mistle2
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
if potion == 7 
	hide hering
	inc potion
	inc score
	"Du wirfst den Hering in den Kessel.",cr,"Der Trank ist Fertig!",cr,"Sofort trinkst du ihn aus.",cr,cr,"WOW! F�hlst du dich jetzt kr�ftig!"
else
	"Du musst den Hering als letzte",cr,"Zutat in den Kessel werfen!"
endif 
# Bonuspunkt
using sword cheese 
	"Oh Nein, der K�se wird nicht aufgeschnitten!",cr,"Dann stinkt das ganze Schwert",cr,"nach dem Zeug!"
using ghoul burger
	hide burger
	inc score
	"Der Ghoul verschlingt schmatzend den",cr,"leckeren Hamburger.",cr,cr,"Das bringt dich aber leider nicht",cr,"weiter.",cr,cr,"Vielleicht h�ttest du ihn vorher",cr,"vergiften sollen?",cr,"Nee, falsches Spiel...",cr,"Das war bei ROBOX..."
using sword herb
	"Man muss Zauberzutaten mit einer",cr,"goldenen Sichel schneiden!"
using sword mistle
	"Man muss Zauberzutaten mit einer",cr,"goldenen Sichel schneiden!"
using herb2 chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using alraun2 chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using mistle2 chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using hering chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using feath chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using fat chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using scumm chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using hair chem
	"Das kannst du hier nicht gebrauchen.",cr,"Das musst du in einen Zauber-",cr,"kessel werfen."
using jemmy coffin2
	"Du willst gerade wieder das Brecheisen",cr,"am Sargdeckel ansetzen,",cr,"entsinnst dich dann aber doch",cr,"anders und l�sst deiner toten Ver-",cr,"wandtschaft ihre Ruhe.",cr,"Mehr als ein Haarb�schel brauchst",cr,"du ja nicht."
## K�mpfe die nicht zum Ziel f�hren
using wand pala
	"Der Palawaum ist gegen Magieschaden",cr,"imun und lacht dich aus!"
using sword kala
	"Der Kalahuii ist gegen physische",cr,"Sch�den imun und verspottet dich!"
using sword ghoul
	move sword tomb
	inc score
	"Gelangweilt haut dir der Ghoul dein",cr,"Schwert aus den H�nden."
using jemmy pala
	move jemmy garden
	inc score
	"Kichernd schnappt sich das Palawaum",cr,"deinen Kuhfuss und rennt damit",cr,"davon.",cr,"Blitzschnell ist es wieder da und",cr,"grinst dich an.",cr,"Dein Brecheisen hat es anscheinend",cr,"irgendwo im Turm versteckt..."
using jemmy kala
	"Du haust dem Kalahuii das Brech-",cr,"eisen auf den Dez.",cr,"Es guckt dich treuherzig an.",cr,"Das scheint ihm gefallen zu haben."
using jemmy ghoul
	"Der Ghoul blockt deinen Angriff",cr,"ohne Probleme ab.",cr,"Mit so einer Waffe kommt man",cr,"dem Kerl nicht bei..."
using wand ghoul
	"Der Ghoul guckt dich nur dumm an.",cr,cr,"Deine �blichen  Zauberspr�che scheinen",cr,"bei dem gar nichts zu bringen."
using sword raven
	"Der Rabe flattert dir davon, als",cr,"er Dich mit dem Schwert an-",cr,"kommen sieht.",cr,"Der scheint clever zu sein."	
using jemmy raven
	"Der Rabe flattert vor dir davon, als",cr,"er Dich mit dem Brecheisen",cr,"sieht.",cr,"Der will wohl nicht gekeult werden.",cr,"Irgendwie auch verst�ndlich..."	
using wand raven
	"Du fuchtelst mit deinem Zauberstab.",cr,"Es knistert nur ein wenig.",cr,"Der Vogel scheint etwas Besonderes",cr,"zu sein. So klappt das nicht."
using spade pala
	"Mit einem Spaten?",cr,"Besorg dir eine bessere Waffe!"
using spade ghoul
	"Der Ghoul schmeisst sich weg vor",cr,"lachen, als du unbeholfen mit dem",cr,"Spaten auf ihn einschlagen willst."
using spade raven
	"Der Rabe kr�ht und faucht dich w�tend",cr,"an, als du mit dem dem Spaten",cr,"auf ihn losgehen willst.",cr,cr,"Erschrocken weichst du einen Schritt",cr,"zur�ck."

# procedures:
#defproc name
# locations:
loc start
	"Flur im Erdgeschoss",cr
	"Du stehst im Eingangsbereich deines",cr
	"Magierturmes.",cr
	"Im S�den befindet sich die Haust�r,",cr
	"nach Osten und Westen f�hren Durch-",cr
	"g�nge. Im Norden des Raumes f�hrt",cr
	"eine steinerne Treppe in die oberen",cr
	"Stockwerke oder hinab in den Keller.",cr
	w2 kitchen
	e2 bathroom
	s2 garden
	d2 tomb
	u2 floor1

loc floor1
	"Flur im ersten Stock",cr
	"Du befindest Dich in einem kleinen",cr
	"Treppenhaus, in dem sich die steinerne",cr
	"Treppe nach sowohl nach oben als nach",cr
	"unten weiter windet. Es ist hier zwar",cr
	"weder kalt noch muffig, aber doch",cr
	"etwas trostlos. Ein schwacher Licht-",cr
	"schimmer dringt aus einem Durchgang im",cr
	"Osten. Eine T�r aus dunklem Holz f�hrt",cr
	"nach Westen.",cr
	w2 study
	e2 bedroom
	u2 floor2

loc floor2
	"Flur im zweiten Stock",cr
	"Eng windet sich die Wendeltreppe nach",cr
	"oben und unten. Du fragst Dich, wann",cr
	"die Treppe endlich ein Ende hat. Ein",cr
	"kleiner Nebengang f�hrt nach Westen,",cr
	"im Osten befindet sich eine h�lzerne",cr
	"T�re mit Eisenbeschl�gen. Ein kleines",cr
	"Fenster spendet etwas Licht.",cr
	w2 laboratory
	e2 library
	u2 observatory

loc observatory
	"Observatorium",cr
	"Hier oben im Observatorium deines Turms",cr
	"hast Du einen grossartigen Blick ueber",cr
	"den Zauberwald. Im Westen siehst Du die",cr
	"ber�hmten Silberberge mit ihren schnee-",cr
	"bedeckten Gipfeln. Der Ausblick l�sst",cr
	"Dich den beschwerlichen Aufgang �ber",cr
	"die Wendeltreppe vergessen. Ein ein-",cr
	"facher Tisch mit einem h�lzernen Stuhl",cr
	"sind neben deinem Teleskop die einzigen",cr
	"Einrichtungsgegenst�nde hier.",cr

loc tomb
	"Gruft",cr
	"Du bist nun in einem uralten, unter-",cr
	"irdischen Grabgew�lbe, der Gruft in der",cr
	"deine Ahnen ruhen. Zu beiden Seiten",cr
	"stehen alte Grabsteine, deren In-",cr
	"schriften nicht mehr zu entziffern",cr
	"sind. Die W�nde bestehen aus gemauertem",cr
	"Stein, der von Moder �berzogen ist.",cr
	"Eine ideale Umgebung f�r alle",cr
	"Kreaturen, die das Licht scheuen.",cr
	"Mitten im Raum steht ein schlichter",cr
	"Altar, an der Nordmauer ist ein Sarg",cr
	"abgestellt.",cr

loc garden
	"Kr�utergarten", cr
	"Du stehst in einem kleinen, h�bschen", cr
	"Vorgarten. Der Garten ist von einem",cr
	"kleinen Zaun umgeben. Unmittelbar",cr
	"dahinter beginnt im S�den das Moder-",cr
	"moor, w�hrend der Turm von allen",cr
	"anderen Seiten vom Salamanderwald",cr
	"eingeschlossen ist. Neben einem",cr
	"Blumenbeet siehst Du vor allem",cr
	"mehrere Kr�uterbeete.",cr
	"Nach Norden kannst du deinen", cr
	"Magierturm betreten.",cr

loc kitchen
	"K�che", cr
	"Hier in der K�che bereit deine Ehegat-",cr
	"tin ihre leckeren Sachen zu. Unter",cr
	"Kennern sind ihre Kochk�nste weit be-",cr
	"kannt. Leider ist sie momentan auf",cr
	"Reisen. Du siehst einen Herd, einen",cr
	"K�chenschrank, einen Tisch und St�hle.",cr
	"Neben dem Herd ist eine Sp�le. An",cr
	"einer Wand h�ngt ein Regal. Im S�den",cr
	"steht die Schlafpritsche deines",cr
	"Lehrlings.", cr

loc bathroom
	"Badezimmer", cr
	"Das ist der Baderaum. Eine Dusche steht",cr
	"in einer Ecke. �ber dem Waschbecken",cr
	"kannst Du einen Spiegel erkennen. Die",cr
	"Badematte am Boden ist feucht, wahr-",cr
	"scheinlich wurde hier vor kurzem gerade",cr
	"geduscht. Ein kleiner Schemel und ein",cr
	"h�lzerner Eimer stehen im Raum.", cr

loc study
	"Wohn- und Studienzimmer", cr
	"Eine Vitrine, ein Regal und ein ab-", cr
	"schliessbares Schr�nkchen h�ngen hier",cr
	"in deinem Wohnzimmer an den W�nden.",cr
	"Ein magischer Schreibtisch, der aus-",cr
	"sieht, als ob er aus einem riesigen",cr
	"Tigerauge gefertigt wurde, befindet",cr
	"sich in der Mitte des Raumes. Dann",cr
	"steht da noch ein bequemer Sessel",cr
	"beim Kamin an der Westwand. Ein",cr
	"Durchgang f�hrt zur�ck nach Osten.", cr

loc bedroom
	"Schlafzimmer",cr
	"Das Schlafzimmer ist recht spartanisch",cr
	"eingerichtet. An der S�dwand steht ein",cr
	"grosses Bett, an der Ostwand ein rie-",cr
	"sieger Schrank. Rund um das Bett ist",cr
	"ein L�ufer ausgelegt und neben dem Bett",cr
	"steht ein kleines Nachtschr�nkchen.",cr
	"Eine T�r aus schwerem Holz f�hrt im",cr
	"Westen zur�ck ins Treppenhaus.",cr

loc laboratory
	"Alchemie-Labor", cr
	"Du bist in einem Turmzimmer gelandet,",cr
	"das �ber und �ber mit merkw�rdigen",cr
	"Apparaten gef�llt ist. Da brodelt,",cr
	"funkt und zischt es, dass es eine reine",cr
	"Freude ist. Nat�rlich weiss ein Fach-",cr
	"mann wie du genauestens Bescheid, wozu",cr
	"die Apparate dienen, die auf dem Tisch",cr
	"stehen. In manchen brodeln Dir wohl-",cr
	"bekannte Chemikalien vor sich hin. Sie",cr
	"sehen wundersch�n giftig aus. Nach",cr
	"Osten kannst du den Raum durch eine",cr
	"T�r verlassen.",cr

loc library
	"Bibliothek", cr
	"An s�mtlichen W�nden des Raumes stehen",cr
	"Regale bis unter die Decke, und alle",cr
	"Regale sind mit B�chern und anderen",cr
	"Schriftst�cken vollgestopft. Wie soll",cr
	"ein zerstreuter Zauberer hier bloss",cr
	"finden, wonach er sucht?",cr
	"Ohne Bibliothekar erscheint Dir das",cr
	"beinahe aussichtslos.", cr


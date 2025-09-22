#!/usr/bin/env python3

import sys

def open_for_reading(filename, encoding):
    """wrapper fn to get nicer error message"""
    try:
        fd = open(filename, "rt", encoding=encoding)
    except Exception as e:
        sys.exit("Error: Cannot open input file: " + str(e))
    return fd

def check_encoding(filename, encoding):
    """check if file adheres to ASCII/UTF8/other limitations"""
    fd = open_for_reading(filename, encoding)
    #print("Trying", encoding)
    with fd as fd:
        try:
            contents = fd.readlines()
        except UnicodeDecodeError as e:
            return False
    return True

def find_encoding(filename):
    """find out if file is UTF-8 or not"""
    if check_encoding(filename, "ascii"):
        return "ascii"
    if check_encoding(filename, "utf-8"):
        return "utf-8"
    # at this point we can't really tell all the remaining 8-bit encodings
    # apart. I guess iso-8859/1 would be the most likely, so let's use the
    # Windows-style superset just in case some of the fancy quotes were used:
    if check_encoding(filename, "cp1252"):
        return "cp1252"
    # this is more or less impossible:
    sys.exit("Error: Encoding of input file not recognized.")

#   list of classes linked to name:
#       line_keyword?   (defined at startup, body is function to handle line)
#       userdefined (defined by user in file: has line number)  except PLAYER, INVENTORY, etc...
#           const?
#           symbol  (has start value) used for vars and fakevars
#               variable
#               literalnumber   (fake var)
#               moveable    (has game name, weight, description)
#                   item    (must gain description code)
#                   npc (has talkto method)
#           usage   (has item and scriptcode)
#           combi   (has items and scriptcode)
#           talkto      FIXME - add way for user to define this!
#           procedure
#           location    (has directions)
#       scriptcode (was codeseq, has output method, code, indents)
# FIXME: atm, items i1 and i2 cannot reference each other in their descriptions:
#   the undefined item is thought to be a location!
#   so either add a possibility to define the description code long after the item,
#   or add some sort of "declare item" line!
#   option 1 seems natural because I need something like that anyway to implement npc's "talkto",
#   but option 2 seems simpler because option 1 would need some way to indicate "no code here, defined later!"
# TODO: cleanup line "preprocessor"

MAX_ERROR_COUNT = 5 # give up after this many errors

# mapping operators from source format to macro format:
operators = {
    '==': 'equal',
    '!=': 'not_equal',
    '<': 'smaller',
    '>': 'greater',
    '<=': 'smaller_or_equal',
    '>=': 'greater_or_equal',
    '@': 'equal',       # actually "at", specially handled
    '!@': 'not_equal'   # actually "not at", specially handled
}
inverted_operators = {
    'equal':        'not_equal',
    'not_equal':    'equal',
    'smaller':      'greater_or_equal',
    'greater':      'smaller_or_equal',
    'smaller_or_equal': 'greater',
    'greater_or_equal': 'smaller'
}


def nospace(string):
    """helper function to remove leading/trailing spaces"""
    return string.split()[0]


def message(msg):
    print(msg, file=sys.stderr)


def warning(msg):
    message('Warning: ' + msg)


class stringcoll(object):
    """collects strings so multiple copies are only put into assembler source once"""

    def __init__(self):
        self.dict = dict()

    def add(self, string):
        """convert string to label"""
        if string in self.dict:
            return self.dict[string]

        # FIXME - add code to check if one endswith() another
        label = 'string_' + str(len(self.dict))
        self.dict[string] = label
        return label

    def get_all(self):
        all = []
        for e in self.dict:
            all.append([self.dict[e], e])
        all.sort()
        return all


def asmlabel_location(name):
    """returns assembler label associated with location name
    this is defined outside of "location" class because it might be needed before location is defined"""
    return 'location_' + name


def asmsymbol_symbol(name):
    """returns assembler symbol associated with script symbol
    this is defined outside of "symbol" class because it might be needed before symbol is defined"""
    return 'vo_' + name


class userdefined(object):
    """parent class for everything defined in game description file"""

    def __init__(self, name):
        self.name = name    # symbolic name
        self.defline = None # line number of definition


class symbol(userdefined):
    """parent class for npc, item, variable and literalnumber"""
    def __init__(self, name, default):
        super(symbol, self).__init__(name)
        self.default = default  # default value at start of game
    def offset_symbol(self):
        return asmsymbol_symbol(self.name)


class variable(symbol):
    """game var scripts can use"""


class literalnumber(symbol):
    """pseudo var to hold literal, the name for e.g. 5 would be "5"."""


class moveable(symbol):
    """things that can move in the game - namely items and npcs"""

    def __init__(self, name, start_location, weight, game_name):
        super(moveable, self).__init__(name, default = 'location_' + start_location)
        self.game_name = game_name
        self.weight = weight
        self.description = None

    def set_description(self, code):
        self.description = code

    def description_label(self):
        return 'itde_' + self.name

    def output_description(self):
        print(self.description_label())
        self.description.output('+end_itemdesc')


class item(moveable):
    """game item player can interact with"""


class npc(moveable):
    """non-player characters - just like items, but player can talk to them"""

    def __init__(self, name, start_location, weight, game_name):
        super(npc, self).__init__(name, start_location, weight, game_name)
        self.talkto = None

    def set_talkto(self, code):
        self.talkto = code

    def talkto_label(self):
        return 'npctalk_' + self.name

    def output_talkto(self):
        print(self.talkto_label())
        self.talkto.output('+end_npctalk')


class scriptcode(object):
    """parent class for all script code sequences"""

    def __init__(self):
        super(scriptcode, self).__init__()
        self.code = []  # holds lines for assembler
        self.indents = 2

    def change_indent(self, n):
        self.indents += n

    # actually do something:
    def add_label(self, line):
        self.code.append(line)

    def add_code(self, line):
        self.code.append(self.indents * '\t' + line)

    def set_dir(self, dir, target):
        self.code.append(self.indents * '\t' + '+' + dir + ' ' + asmlabel_location(target))
        # TODO - add warning if direction has already been set on outermost block level!
        # self.warning_line('Direction "' + direction + '" was already set')

    def output(self, endcmd):
        for line in self.code:
            print(line)
        print(self.indents * '\t' + endcmd)


class procedure(userdefined):
    """callable code"""

    def __init__(self, name):
        super(procedure, self).__init__(name)
        self.code = None

    def set_code(self, code):
        self.code = code

    def code_label(self):
        return 'proc_' + self.name

    def output(self):
        print(self.code_label())
        self.code.output('+end_procedure')


class usage(userdefined):
    """what to do when player enters USE A"""

    def __init__(self, hinz):
        super(usage, self).__init__('usage ' + hinz)
        self.hinz = hinz
        self.code = None

    def set_code(self, code):
        self.code = code

    def output(self):
        print('\t!wo +\t; link pointer')
        print('\t!by ' + asmsymbol_symbol(self.hinz))
        self.code.output('+end_use')


class combi(userdefined):
    """what to do when player enters COMBINE A WITH B"""

    def __init__(self, hinz, kunz):
        super(combi, self).__init__('combi ' + hinz + ' ' + kunz)
        self.hinz = hinz
        self.kunz = kunz
        self.code = None

    def set_code(self, code):
        self.code = code

    def output(self):
        print('\t!wo +\t; link pointer')
        print('\t+ordered ' + asmsymbol_symbol(self.hinz) + ', ' + asmsymbol_symbol(self.kunz))
        self.code.output('+end_combi')


class location(userdefined):
    """location definition"""

    def __init__(self, name):
        super(location, self).__init__(name)
        self.forced_value = None    # only used for "NOWHERE" and "INVENTORY"
        self.code = None

    def set_code(self, code):
        self.code = code

    def set_forced_value(self, value):
        self.forced_value = value

    def code_label(self):
        return asmlabel_location(self.name)

    def output(self, extdirdict):
        if self.forced_value != None:
            print('!addr\t' + self.code_label() + '\t= ' + str(self.forced_value) + '\t; pseudo location')
        else:
            print(self.code_label())
            for dir in extdirdict:
                print(self.code.indents * '\t' + '+' + dir + ' ' + asmlabel_location(extdirdict[dir]) + '\t; autocreated by target')
            self.code.output('+end_location')


class converter(object):
    """converts MCA2 source to ACME source"""

    def __init__(self):
        self.error_count = 0    # converter stops when this exceeds MAX_ERROR_COUNT
        self.in_comment = False # for c-style multi-line comments
        self.text_mode = False  # needed to add command prefix and trailing NUL char
        self.codeseq = None # needed to track locations/procedures/combinations/usages
        self.block_state = [0]  # keeps track of "while/endwhile/if/elif/else/endif" and nesting
        self.code = []  # for stuff from "asm" lines
        self.subst = dict() # dictionary for "define/enum" substitutions    FIXME - move to some input preprocessor
        self.stringcoll = stringcoll()
        self.definitions = dict()   # maps object names to objects
        self.ordered_defs = []  # helper list so order of definitions is kept
        self.references = dict()
        self.current_location = None    # name of "current" location, for backlinks
        self.musthaves = {} # collects a few flags so user can be told what is missing

        # create some pre-defined stuff:
        # special value for lines below
        self.line_number = '<predefined>'
        # create pseudo npc 'PLAYER'
        PLAYER_npc = npc('PLAYER', start_location = 'start', weight = '$80', game_name = 'nullstring')
        PLAYER_npc.set_description(scriptcode())
        PLAYER_npc.set_talkto('nullstring')
        # create pseudo location "NOWHERE" to be able to hide npcs/items and disable directions
        NOWHERE_location = location('NOWHERE')
        NOWHERE_location.set_forced_value(0)
        # create pseudo location "INVENTORY" where npcs/items can be moved
        INVENTORY_location = location('INVENTORY')
        INVENTORY_location.set_forced_value(1)
        # create pseudo vars:
        TMP_var = variable('__TMP__', '0')  # for holding literal
        RND_var = variable('RANDOM', '0')   # for random number
        TIME_var = variable('TIME_s', '0')  # for holding seconds counter
        # register definitions
        self.add_symbol_definition(PLAYER_npc)
        self.add_symbol_definition(NOWHERE_location)
        self.add_symbol_definition(INVENTORY_location)
        self.add_symbol_definition(TMP_var)
        self.add_symbol_definition(RND_var)
        self.add_symbol_definition(TIME_var)
        # make sure some things are marked as referenced even if not ref'd in script, to inhibit confusing errors
        self.add_symbol_reference('intro', procedure)
        self.add_symbol_reference('start', location)
        self.add_symbol_reference('INVENTORY', location)
        self.add_symbol_reference('NOWHERE', location)
        self.add_symbol_reference('PLAYER', npc)
        self.add_symbol_reference('__TMP__', variable)
        self.add_symbol_reference('RND', variable)
        self.add_symbol_reference('TIME', variable)
        # correct start value for later
        self.line_number = 0

    def add_symbol_definition(self, obj):
        if obj.name in self.definitions:
            self.error_line('object "' + obj.name + '" already defined in line ' + str(self.definitions[obj.name].defline))
        # if there is already a reference to it, type must match!
        if obj.name in self.references:
            if not issubclass(type(obj), self.references[obj.name]['type']):
                self.error_line('expected object "' + name + '" to be of different type, see line ' + str(self.references[name]['firstrefline']))
        obj.defline = self.line_number
        self.definitions[obj.name] = obj
        self.ordered_defs.append(obj.name)

    def add_symbol_reference(self, name, objtype):
        if name in self.references:
            if issubclass(objtype, self.references[name]['type']):
                # new ref is same type or even more specific
                self.references[name]['type'] = objtype # use more specific one
                return
            if not issubclass(self.references[name]['type'], objtype):
                self.error_line('object type in ref is different from first ref (line ' + str(self.references[name]['firstrefline']) + ')')
                self.error_line(str(objtype) + str(self.references[name]['type']))
        else:
            self.references[name] = {'type': objtype, 'firstrefline' : self.line_number}
            # if obj is location, "backdir" dict may be added to this dict!

    def ensure_defined(self, name, objtype):
        if name not in self.definitions:
            self.error_line('object "' + name + '" used but not defined.')
            return

        if not isinstance(self.definitions[name], objtype):
            self.error_line('object "' + name + '" is of wrong type (defined on line ' + str(self.definitions[name].defline) + ').')
            return

        self.add_symbol_reference(name, objtype)
        return self.definitions[name]

    def get_defined(self, objtype):
        """return list of all defined objects of the given type"""
        list = []
        for key in self.ordered_defs:
            obj = self.definitions[key]
            if type(obj) == objtype:
                list.append(obj)
        return list

    def get_defd_and_refd(self, objtype):
        """return list of all defined objects of the given type that were actually referenced"""
        list = []
        for key in self.ordered_defs:
            obj = self.definitions[key]
            if type(obj) == objtype and key in self.references:
                list.append(obj)
        return list

    def error(self, msg):
        message('Error: ' + msg)
        self.error_count += 1
        if self.error_count >= MAX_ERROR_COUNT:
            sys.exit("Giving up.")

    def warning_line(self, msg):
        warning('in line %d: %s!' % (self.line_number, msg))

    def error_line(self, msg):
        self.error('in line %d: %s!' % (self.line_number, msg))

#    def err_serious_line(self, msg):
#        print >> sys.stderr, 'Serious error in line %d: %s!' % (self.line_number, msg)
#        sys.exit(1)

    def add_location_direction(self, direction, target_name):
        """add direction possibility to current location"""
        self.add_symbol_reference(target_name, location)
        self.codeseq.set_dir(direction, target_name)

    def add_location_backdirection(self, target_name, direction):
        """add current location as direction possibility to other location
        (when going from target_name in direction, result is current_location)"""
        self.add_symbol_reference(target_name, location)
        self.add_symbol_reference(self.current_location, location)
        # if there is no backdir dict yet, create one:
        if 'backdir' not in self.references[target_name]:
            self.references[target_name]['backdir'] = dict()
        # get backdir dict
        locdict = self.references[target_name]['backdir']
        if direction in locdict:
            if locdict[direction] != self.current_location:
                self.warning_line('Back-direction "' + direction + '" was already set for target')
        locdict[direction] = self.current_location

    def get_value(self, string):
        """return value of number literal"""
        try:
            num = int(string)
        except:
            self.error_line('Cannot determine numerical value of "' + string + '"')
            num = 0 # make sure script does not crash
        return num

    def get_force2var(self, string):
        """convert literal/var name string to var object"""
        string = nospace(string)
        if string in self.definitions:
            obj = self.definitions[string]
            if type(obj) == variable:
                self.add_symbol_reference(string, variable)
                return obj  # return var object
            elif type(obj) == literalnumber:
                self.add_symbol_reference(string, literalnumber)
                return obj  # return fakevar object
            else:
                self.error_line('symbol defined on line ' + str(obj.defline) + ' is not a variable')
        # if no var, must be literal - convert to number strings
        value = self.get_value(string)
        fakename = str(value)
        literal = literalnumber(fakename, str(value))
        self.add_symbol_definition(literal)
        self.add_symbol_reference(fakename, literalnumber)
        return literal

    def add_code(self, line):
        """this is for "asm" lines and other stuff not part of specific code sequences like procedures and/or locations"""
        self.code.append('\t' + line)

    def check_refs_FIXME(self, dict, name):
        for thing in dict.get_undefd_and_refd():
            self.error(name + ' referenced but not defined: ' + thing.name)
            #if loc.line_of_def and not loc.referenced:
            #    warning('location "' + loc.name + '" defined but never used')
            #if loc.referenced and not loc.line_of_def:
            #    self.error('location "' + loc.name + '" referenced but not defined')

    def output(self):
#        self.check_refs(self.npcs, 'npc')
#        self.check_refs(self.items, 'item')
#        self.check_refs(self.vars, 'variable')
#        self.check_refs(self.procedures, 'procedure')
#        self.check_refs(self.locations, 'location')
        print(';ACME 0.97')
        print(';')
        print('; DO NOT EDIT THIS FILE! THIS FILE IS AUTOMATICALLY GENERATED!')
        print(';')

        # symbol definitions are given first:

        print('; stuff generated by "asm" lines:')
        for line in self.code:
            print(line)
        print()

        var_index = 0
        print('; var offsets:')
        print('\t; npcs:')
        for npcs in self.get_defined(npc):  # use unref'd npcs as well, they might be red herrings
            print('\t' + npcs.offset_symbol() + '\t= ' + str(var_index) + '\t; default value is', npcs.default)
            var_index += 1
        print('\tgamevars_NPCCOUNT\t=', var_index)   # == len(self.npcs)
        print('\t; items:')
        for it in self.get_defined(item):   # use unref'd items as well, they might be red herrings
            print('\t' + it.offset_symbol() + '\t= ' + str(var_index) + '\t; default value is', it.default)
            var_index += 1
        print('\tgamevars_ITEMCOUNT\t=', var_index)  # == len(self.npcs) + len(self.items)
        print('\t; game vars:')
        for var in self.get_defd_and_refd(variable):
            print('\t' + var.offset_symbol() + '\t= ' + str(var_index) + '\t; default value is', var.default)
            var_index += 1

        print('\tgamevars_SAVECOUNT\t=', var_index)  # == len(self.npcs) + len(self.items) + len(self.vars)
        print('\t; fake vars (literals):')
        for fakevar in self.get_defd_and_refd(literalnumber):
            print('\t' + fakevar.offset_symbol() + '\t= ' + str(var_index))
            var_index += 1
        print('\tgamevars_COUNT\t=', var_index)  # == len(self.npcs) + len(self.items) + len(self.vars) + len(self.fakevars)
        print()

        # all data tables are put into macro so backend can put where needed:

        print('!macro game_tables {')
        print()

        npcs_defaults = [str(npcs.default) for npcs in self.get_defined(npc)]   # use unref'd npcs as well, they might be red herrings
        items_defaults = [str(it.default) for it in self.get_defined(item)] # use unref'd items as well, they might be red herrings
        vars_defaults = [str(symbol.default) for symbol in self.get_defd_and_refd(variable)]
        fakevars_defaults = [str(symbol.default) for symbol in self.get_defd_and_refd(literalnumber)]
        print('gamevars_defaults_lo')
        print('\t!by <' + ', <'.join(npcs_defaults) + '\t; npcs')
        print('\t!by <' + ', <'.join(items_defaults) + '\t; items')
        print('\t!by <' + ', <'.join(vars_defaults) + '\t; variables')
        if len(fakevars_defaults):
            print('\t!by <' + ', <'.join(fakevars_defaults) + '\t; literals')
        print('gamevars_defaults_hi')
        print('\t!by >' + ', >'.join(npcs_defaults) + '\t; npcs')
        print('\t!by >' + ', >'.join(items_defaults) + '\t; items')
        print('\t!by >' + ', >'.join(vars_defaults) + '\t; variables')
        if len(fakevars_defaults):
            print('\t!by >' + ', >'.join(fakevars_defaults) + '\t; literals')
        print()

        # npc/item weights
        print('; npc/item weights:')
        print('npcitem_weight')
        npc_weights = [npcs.weight for npcs in self.get_defined(npc)]   # use unref'd npcs as well, they might be red herrings
        print('\t\t!by ' + ', '.join(npc_weights) + '\t; npcs')
        item_weights = [it.weight for it in self.get_defined(item)] # use unref'd items as well, they might be red herrings
        print('\t\t!by ' + ', '.join(item_weights) + '\t; items')
        print()

        # pointer arrays and actual strings
        print('; string pointers:')
        npc_names = [npcs.game_name for npcs in self.get_defined(npc)]  # use unref'd npcs as well, they might be red herrings
        item_names = [it.game_name for it in self.get_defined(item)]    # use unref'd items as well, they might be red herrings
        print('npcitem_name_lo\t!by <' + ', <'.join(npc_names) + '\t; npcs')
        print('\t\t!by <' + ', <'.join(item_names) + '\t; items')
        print('npcitem_name_hi\t!by >' + ', >'.join(npc_names) + '\t; npcs')
        print('\t\t!by >' + ', >'.join(item_names) + '\t; items')
        print('; strings:')
        for label, string in self.stringcoll.get_all():
            print(label + '\t!tx ' + string + ', 0')
        print()

        # npc/item description pointers
        print('; npc/item description pointers:')
        npc_descs = [npcs.description_label() for npcs in self.get_defined(npc)]    # use unref'd npcs as well, they might be red herrings
        item_descs = [it.description_label() for it in self.get_defined(item)]  # use unref'd items as well, they might be red herrings
        print('npcitem_desc_lo\t!by <' + ', <'.join(npc_descs) + '\t; npcs')
        print('\t\t!by <' + ', <'.join(item_descs) + '\t; items')
        print('npcitem_desc_hi\t!by >' + ', >'.join(npc_descs) + '\t; npcs')
        print('\t\t!by >' + ', >'.join(item_descs) + '\t; items')
        # FIXME - solve weight/size issue: split items into two groups to get rid of lookup table?
        # FIXME - in future, iterate over items twice and do mobile/fixed items separately?
        print()

        print('; npc descriptions:')
        for npcs in self.get_defined(npc):  # use unref'd npcs as well, they might be red herrings
            npcs.output_description()
            print()

        print('; item descriptions:')
        for it in self.get_defined(item):   # use unref'd items as well, they might be red herrings
            it.output_description()
            print()

        print('; usages:')
        print('usages')
        for use in self.get_defined(usage):
            use.output()
            print('+')
        print('\t!wo 0\t; end marker')
        print()
        print('; combinations:')
        print('combis')
        for co in self.get_defined(combi):
            co.output()
            print('+')
        print('nullstring\t!wo 0\t; end marker (doubles as "nullstring" terminator)')
        print()
        print('; procedures:')
        for proc in self.get_defd_and_refd(procedure):
            proc.output()
            print()
        print('; locations:')
        for loc in self.get_defd_and_refd(location):
            if 'backdir' in self.references[loc.name]:
                loc.output(self.references[loc.name]['backdir'])
            else:
                loc.output(dict())
            print()

        print('; end of actual data')
        print()
        print('} ; end of macro')
        print('!eof')
        #print 'debugging info:'
        print('; end of auto-generated file')

    # helper functions to parse lines:
    def preprocess(self, line_in):
        """remove comments, return remainder of line as a list of tokens"""
        result = []
        token = ''
        quotes = None
        for char in line_in:
            cc = ord(char)
            # do not change anything inside strings:
            if quotes != None:
                # we're inside quotes
                # FIXME - check for backslash escapes!
                token += char
                # check for end of quotes:
                if cc == quotes:
                    quotes = None   # found end of quotes
                    result.append(token)
                    token = ''
                continue
            # we're not inside quotes, so check for quotes:
            if cc == 34 or cc == 39:
                quotes = cc
                # start a new token:
                if token:
                    result.append(token)
                token = char
                continue    # do not remove '#' in strings
            # check for comments:
            if cc == 35:
                break   # remove comment
            # whitespace? then start a new token:
            if cc == 32 or cc == 9:
                if token:
                    result.append(token)
                    token = ''
                continue
            # TODO: add checks so "identifier=9" is split into three tokens!
            token += char
        if quotes != None:
            self.error_line('quotes still open at end of line')
        if token:
            result.append(token)
        # subst
        for idx in range(0, len(result)):
            result[idx] = self.subst.get(result[idx], result[idx])
        return result

    def get_args(self, line, howmany):
        """ensure correct number of args and return them"""
        if len(line) < 1 + howmany:
            self.error_line('Too few arguments for keyword')
        elif len(line) > 1 + howmany:
            self.error_line('Too many arguments for keyword')
        return line[1:(1 + howmany)]

# helper functions to open/close logical blocks:
    def text_close(self):
        """if we are in text mode, terminate"""
        if self.text_mode:
            self.codeseq.add_code('+terminate')
            self.text_mode = False

    def code_open(self):
        sc = scriptcode()
        self.codeseq = sc
        return sc

    def code_close(self):
        """if we are in description/location/procedure/usage/combination, terminate"""
        self.text_close()
        if self.codeseq != None:
            if self.block_state != [0]:
                self.error_line('cannot start new description/location/procedure/usage/combination, there are "if" or "while" blocks left open')
            self.codeseq = None
        self.current_location = None

# functions to parse different line types:
    # CAUTION: all names starting with "handle_" may be looked up via internal dict,
    # so this code won't necessarily reference them directly!

    def handle_asm_line(self, line):
        """line to pass to assembler unchanged"""
        if self.codeseq != None:
            self.error_line('Please put "asm" lines before all npcs/items/locations/procedures/usages/combinations')
        if line[1] in ("DEUTSCH", "color_std", "color_border", "color_background", "color_emph", "color_out"):
            self.musthaves[line[1]] = True
        self.add_code(' '.join(line[1:]))

    def process_text_line(self, line):
        """text line"""
        if self.text_mode == False:
            self.codeseq.add_code('+print')
            self.text_mode = True
        self.codeseq.add_code('!tx ' + ' '.join(line))

    def handle_use_line(self, line):
        """code to call if player wants to use item"""
        self.code_close()   # close previous code sequence, if there was one
        it = self.get_args(line, 1)[0]
        self.ensure_defined(it, item)
        self.add_symbol_reference(it, item)
        use = usage(it)
        self.add_symbol_definition(use)
        use.set_code(self.code_open())

    def handle_combine_line(self, line):
        """code to call if player wants to combine items"""
        self.code_close()   # close previous code sequence, if there was one
        it1, it2 = self.get_args(line, 2)
        self.ensure_defined(it1, item)
        self.ensure_defined(it2, item)
        self.add_symbol_reference(it1, item)
        self.add_symbol_reference(it2, item)
        co = combi(it1, it2)
        self.add_symbol_definition(co)
        co.set_code(self.code_open())

    def handle_using_line(self, line):
        """older form of "combine" keyword"""
        self.handle_combine_line(line)

    def proc_loc_line(self, line, objtype):
        """new procedure or location"""
        self.code_close()   # close previous code sequence, if there was one
        name = self.get_args(line, 1)[0]
        obj = objtype(name) # create
        self.add_symbol_definition(obj)
        obj.set_code(self.code_open())
        return name

    def handle_loc_line(self, line):
        """new location"""
        self.current_location = self.proc_loc_line(line, location)

    def handle_proc_line(self, line):
        """new procedure"""
        self.proc_loc_line(line, procedure)

    def handle_callproc_line(self, line):
        """call procedure"""
        self.text_close()
        proc_name = self.get_args(line, 1)[0]
        proc = self.ensure_defined(proc_name, procedure)
        self.codeseq.add_code('+gosub ' + proc.code_label())

    def handle_callasm_line(self, line):
        """call machine language"""
        self.text_close()
        asm_name = self.get_args(line, 1)[0]
        self.codeseq.add_code('+callasm ' + asm_name)

    def process_dir_line(self, direction, line, backdir=None):
        """allow a direction of movement and specify target, with two-way option"""
        self.text_close()
        if direction in ('northeast', 'southeast', 'southwest', 'northwest'):
            self.uses_10_directions = True  # FIXME: add a check and error if combined with old mc interface because that only supports six directions (unless playing with numpad)
        target_loc_name = self.get_args(line, 1)[0]
        self.add_location_direction(direction, target_loc_name)
        if backdir:
            if self.current_location == None:
                self.error_line('two-way directions can only be used in "location" blocks')
            elif self.block_state != [0]:
                self.error_line('two-way directions cannot be used in "if"/"while" blocks')
            else:
                self.add_location_backdirection(target_loc_name, backdir)

    # directional movements
    def handle_n_line(self, line):
        self.process_dir_line('north', line)
    def handle_ne_line(self, line):
        self.process_dir_line('northeast', line)
    def handle_e_line(self, line):
        self.process_dir_line('east', line)
    def handle_se_line(self, line):
        self.process_dir_line('southeast', line)
    def handle_s_line(self, line):
        self.process_dir_line('south', line)
    def handle_sw_line(self, line):
        self.process_dir_line('southwest', line)
    def handle_w_line(self, line):
        self.process_dir_line('west', line)
    def handle_nw_line(self, line):
        self.process_dir_line('northwest', line)
    def handle_u_line(self, line):
        self.process_dir_line('up', line)
    def handle_d_line(self, line):
        self.process_dir_line('down', line)

    # directional movements with two-way shortcut:
    def handle_n2_line(self, line):
        self.process_dir_line('north', line, 'south')
    def handle_ne2_line(self, line):
        self.process_dir_line('northeast', line, 'southwest')
    def handle_e2_line(self, line):
        self.process_dir_line('east', line, 'west')
    def handle_se2_line(self, line):
        self.process_dir_line('southeast', line, 'northwest')
    def handle_s2_line(self, line):
        self.process_dir_line('south', line, 'north')
    def handle_sw2_line(self, line):
        self.process_dir_line('southwest', line, 'northeast')
    def handle_w2_line(self, line):
        self.process_dir_line('west', line, 'east')
    def handle_nw2_line(self, line):
        self.process_dir_line('northwest', line, 'southeast')
    def handle_u2_line(self, line):
        self.process_dir_line('up', line, 'down')
    def handle_d2_line(self, line):
        self.process_dir_line('down', line, 'up')

    def add_substitution(self, name, value):
        """helper function for "define" and "enum" lines"""
        if name in self.definitions:
            self.error_line('Name "' + name + '" has already been assigned to an object in line ' + self.definitions[name].defline)
        else:
            self.subst[name] = value

    def handle_define_line(self, line):
        """definition for text substitution (basically symbolic constants)"""
        #self.text_close()      this can actually be given inside of text as it does not inject code into output!
        name, value = self.get_args(line, 2)
        self.add_substitution(name, value)

    def handle_enum_line(self, line):
        """enumerate symbolic constants"""
        #self.text_close()      this can actually be given inside of text as it does not inject code into output!
        value = 0
        for word in line[1:]:   # remove 'enum' keyword, line is already split at spaces
            self.add_substitution(word, str(value))
            value += 1

    def handle_u16_line(self, line):
        """variable declaration (unsigned 16 bit)"""
        #self.text_close()      this can actually be given inside of text as it does not inject code into output!
        name, start_value = self.get_args(line, 2)
        num = self.get_value(start_value)   # get actual number for start value     FIXME - move this to some pre-processor
        self.add_symbol_definition(variable(name, num))

    def handle_var_line(self, line):
        """older form of "u16" keyword"""
        self.handle_u16_line(line)

    def process_npcitem(self, line, objtype):
        """declare npc or item for player to interact with"""
        self.code_close()   # close previous code sequence, if there was one
        name, initial_location, weight, game_name = self.get_args(line, 4)
        if weight == 'small':   # FIXME - use script's "const" facility for this?
            weight = '0'
        elif weight == 'large':
            weight = '$80'
        else:
            self.error_line('NPC/item size must be "small" or "large"')
        game_name_label = self.stringcoll.add(game_name)
        npcitem = objtype(name, start_location = initial_location, weight = weight, game_name = game_name_label)
        self.add_symbol_definition(npcitem)
        self.add_symbol_reference(initial_location, location)
        # make current
        npcitem.set_description(self.code_open())

    def handle_npc_line(self, line):
        self.process_npcitem(line, npc)

    def handle_item_line(self, line):
        self.musthaves["item"] = True
        self.process_npcitem(line, item)

    def handle_delay_line(self, line):
        """wait for given number of .1 seconds"""
        self.text_close()
        var = self.get_force2var(self.get_args(line, 1)[0]) # arg could be var or const or literal
        self.codeseq.add_code('+delay ' + var.offset_symbol())

    def check_for_moveable(self, name):
        """return TRUE if given name is moveable (npc/item)"""
        if name in self.definitions:
            obj = self.definitions[name]
            return isinstance(obj, moveable)
        if name in self.references:
            infodict = self.references[name]
            return issubclass(infodict['type'], moveable)
        return False

# if/elif/else/endif helpers:
    def process_condition(self, line, label=None, invert=False):
        if len(line) == 2:
            hinz = self.get_args(line, 1)[0]
            op = '!='
            kunz = '0'
        else:
            hinz, op, kunz = self.get_args(line, 3)
        if op in operators:
            oper = operators[op]
        else:
            self.error_line('Comparison not recognised')
            return
        if invert:
            oper = inverted_operators[oper]
        if op.endswith('@'):
            'args are expected to be MOVEABLE/MOVEABLE or MOVEABLE/LOCATION'
            var1 = self.ensure_defined(hinz, moveable)
            if self.check_for_moveable(kunz):
                # arg2 is moveable (already defined)
                self.add_symbol_reference(kunz, moveable)
                var2 = self.definitions[kunz]
            else:
                # arg2 must be location (maybe not defined yet)
                var2 = self.definitions['__TMP__']
                self.add_symbol_reference(kunz, location)
                self.codeseq.add_code('+varloadimm ' + var2.offset_symbol() + ', ' + asmlabel_location(kunz))
        else:
            var1 = self.get_force2var(hinz)
            var2 = self.get_force2var(kunz)
        code = '+if_' + oper + ' ' + var1.offset_symbol() + ', ' + var2.offset_symbol()
        if label is None:
            label = '.c_after' + str(self.block_state[-1])
        self.codeseq.add_code(code + ', ' + label)

    def end_cond_block(self):
        self.codeseq.add_code('+goto .c_end')
        self.codeseq.add_label('.c_after' + str(self.block_state[-1]))

# while/endwhile:
    def handle_while_line(self, line):
        self.text_close()
        self.codeseq.add_code('!zone { ; "while"')  # TODO: get rid of zone. find a way to implement break/continue!
        self.block_state.append(line)   # keep line for later, will be evaluated by "endwhile"
        self.block_state.append("w")    # go deeper, now in "while" block
        self.codeseq.add_code('+goto .c_continue')
        self.codeseq.add_label('.c_loop')
        self.codeseq.change_indent(1)

    def handle_endwhile_line(self, line):
        self.text_close()
        if ' '.join(line) != 'endwhile':
            self.error_line('Garbage after ENDWHILE?!')
        if self.block_state[-1] != "w":
            self.error_line('Used ENDWHILE without WHILE')
            return
        self.block_state.pop()  # leave nesting level (remove "w")
        line = self.block_state.pop()   # get condition
        self.codeseq.add_label('.c_continue')
        self.process_condition(line, '.c_loop', invert=True)
        self.codeseq.change_indent(-1)
        self.codeseq.add_code('} ; end of "while" zone')

# if/elif/else/endif:
    def handle_if_line(self, line):
        self.text_close()
        self.codeseq.add_code('!zone { ; "if/elif/else"')   # TODO: get rid of zone, add an "if" nesting counter to labels instead. I need "zone" for loops/break/continue!
        self.block_state.append(1)  # go deeper, then in 1st block of if/elif/else
        self.process_condition(line)
        self.codeseq.change_indent(1)

    def handle_elif_line(self, line):
        self.text_close()
        if self.block_state[-1] in (0, "w"):
            self.error_line('Used ELIF without IF')
        if self.block_state[-1] == -1:
            self.error_line('Used ELIF after ELSE')
        self.end_cond_block()
        self.block_state[-1] += 1    # in next block of if/elif/else/endif
        self.codeseq.change_indent(-1)
        self.process_condition(line)
        self.codeseq.change_indent(1)

    def handle_else_line(self, line):
        self.text_close()
        if ' '.join(line) != 'else':
            self.error_line('Garbage after ELSE?!')
        if self.block_state[-1] in (0, "w"):
            self.error_line('Used ELSE without IF')
        if self.block_state[-1] == -1:
            self.error_line('Used ELSE after ELSE')
        self.end_cond_block()
        self.codeseq.change_indent(-1)
        self.codeseq.add_code(';else')
        self.codeseq.change_indent(1)
        self.block_state[-1] = -1   # in ELSE block of if/elif/else/endif

    def handle_endif_line(self, line):
        self.text_close()
        if ' '.join(line) != 'endif':
            self.error_line('Garbage after ENDIF?!')
        if self.block_state[-1] == 0:
            self.error_line('Used ENDIF without IF')
        if self.block_state[-1] != -1:
            self.codeseq.add_label('.c_after' + str(self.block_state[-1]))
        self.codeseq.add_label('.c_end')
        self.block_state.pop()  # leave nesting level
        self.codeseq.change_indent(-1)
        self.codeseq.add_code('} ; end of "if/elif/else" zone')

# var changing:
    def handle_move_line(self, line):
        """move an npc/item to a different location
        args are expected to be MOVEABLE/MOVEABLE or MOVEABLE/LOCATION"""
        self.text_close()
        thing, target = self.get_args(line, 2)
        npcitem = self.ensure_defined(thing, moveable)
        if self.check_for_moveable(target):
            # target is moveable (npc or item, already defined)
            self.codeseq.add_code('+varcopy ' + npcitem.offset_symbol() + ', ' + asmsymbol_symbol(target))
        else:
            # target must be location (maybe not defined yet)
            self.add_symbol_reference(target, location)
            # FIXME - check for "large" item and "INVENTORY" target and complain?
            # but still the problem remains if moving large item @ small item in INV!
            self.codeseq.add_code('+varloadimm ' + npcitem.offset_symbol() + ', ' + asmlabel_location(target))

    def handle_gain_line(self, line):
        """move an npc/item to INVENTORY"""
        npcitem = self.get_args(line, 1)[0]
        self.handle_move_line(['move', npcitem, 'INVENTORY'])

    def handle_hide_line(self, line):
        """move an npc/item to NOWHERE"""
        npcitem = self.get_args(line, 1)[0]
        self.handle_move_line(['move', npcitem, 'NOWHERE'])

    def process_let_line(self, line):
        """writing to variable"""
        self.text_close()
        # arg checking was done by caller, to be able to recognize this type of line...
        target_varname = nospace(line[0])
        target_var = self.ensure_defined(target_varname, variable)
        source_var = self.get_force2var(line[2])
        # FIXME - make sure target var is not read-only!
        self.codeseq.add_code('+varcopy ' + target_var.offset_symbol() + ', ' + source_var.offset_symbol())

    def process_incdec_line(self, what, line):
        """increment/decrement variable"""
        self.text_close()
        varname = self.get_args(line, 1)[0]
        var = self.ensure_defined(varname, variable)
        # FIXME - make sure var is not read-only!
        self.codeseq.add_code('+' + what + ' ' + var.offset_symbol())

    # increment/decrement variable
    def handle_inc_line(self, line):
        self.process_incdec_line('varinc', line)
    def handle_dec_line(self, line):
        self.process_incdec_line('vardec', line)

# outer stuff:
    def process_line(self, line):
        """process a single line of input"""
        self.line_number += 1
        # if there is a BOM, ignore it
        # (only really needed for first line of file)
        if len(line) and line[0] == chr(0xfeff):
            line = line[1:]
        # remove (CR)LF:
        if len(line) and line[-1] == '\n':
            line = line[:-1]
        if len(line) and line[-1] == '\r':
            line = line[:-1]
        line = self.preprocess(line)
        # ignore empty lines
        if line == []:
            return
        # handle end of multi-line comment:
        if self.in_comment:
            if line[0].startswith('*/'):
                self.in_comment = False
            return
        if line[0].startswith('/*'):
            # start of multi-line comment
            self.in_comment = True
            return
        elif line[0].startswith('"') or line[0].startswith("'"):
            # text output
            self.process_text_line(line)
        else:
            if len(line) == 3 and line[1] == '=':
                # everything else should be an assignment to a variable...
                self.process_let_line(line)
            else:
                # ...or start with a keyword:
                handler = getattr(converter, "handle_" + line[0] + "_line", None)
                if handler:
                    handler(self, line)
                else:
                    self.error_line('Line type not recognised')
        #debug:
        #self.codeseq.code.append(line)

    def parse_file(self, filename):
        encoding = find_encoding(filename)
        with open_for_reading(filename, encoding=encoding) as file:
            for line in file:
                self.process_line(line)
            self.code_close()   # make sure last text/code sequence is terminated
        if self.error_count:
            sys.exit(1) # give up because of error(s)
        # check must-haves:
        if "DEUTSCH" not in self.musthaves:
            sys.exit('You need a "asm DEUTSCH = 0" (or 1) line in your game definition file.')
        if "item" not in self.musthaves:
            sys.exit('You need to define at least one item in your game definition file.')
        for color in ("color_std", "color_border", "color_background", "color_emph", "color_out"):
            if color not in self.musthaves:
                sys.exit("You need to define " + color + " in your game definition file.")
        if "intro" not in self.definitions:
            sys.exit('You need to define "proc intro" in your game definition file.')
        if "start" not in self.definitions:
            sys.exit('You need to define "loc start" in your game definition file.')


if __name__ == '__main__':
    sys.exit("This file is a library, it cannot be run.")

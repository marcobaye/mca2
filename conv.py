#!/usr/bin/python2
import sys

operators = {
	'==': 'equal',
	'!=': 'not_equal',
	'<': 'smaller',
	'>': 'greater',
	'<=': 'smaller_or_equal',
	'>=': 'greater_or_equal',
	'@': 'equal',		# actually "at", specially handled
	'!@': 'not_equal'	# actually "not at", specially handled
}

def nospace(string):
	'helper function to remove leading/trailing spaces'
	return string.split()[0]

def message(msg):
	print >> sys.stderr, msg
def warning(msg):
	message('Warning: ' + msg)

class mydict(dict):
	'helper class for object dictionaries'
	def __init__(self, constructor):
		super(mydict, self).__init__()
		self.constructor = constructor
		self.defined = []
		self.referenced = []
	def define(self, obj):
		self.defined.append(obj)
	def reference(self, obj):
		self.referenced.append(obj)
	def get_defined(self):
		return self.defined[:]
	def get_defd_and_refd(self):
		ret = []
		for obj in self.defined:
			if obj.referenced:
				ret.append(obj)
		return ret
	def get_undefd_and_refd(self):
		ret = []
		for obj in self.referenced:
			if obj not in self.defined:
				ret.append(obj)
		return ret
	def get_referenced(self):
		ret = []
		for obj in self.referenced:
			ret.append(obj)
		return ret

class stringcoll(object):
	'collects strings so multiple copies are only put into assembler source once'
	def __init__(self):
		self.dict = dict()
	def add(self, string):
		'convert string to label'
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

class mca2obj(object):
	'parent class for everything defined in game description file'
	def __init__(self, name):
		self.name = name	# symbolic name
		self.referenced = False	# for debugging output ("object XYZ never used!")
	def reference(self):
		self.referenced = True

class symbol(mca2obj):
	'parent class for item, var and fakevar'
	def __init__(self, name):
		super(symbol, self).__init__(name)
		self.default = None	# default value at start of game
	def offset_name(self):
		return 'vo_' + self.name
	def set_default(self, value):
		self.default = value

class item(symbol):
	'game item player can interact with'
	def __init__(self, name):
		super(item, self).__init__(name)
		self.game_name = None
		self.weight = 0
		self.description = itemdesc(name)
	def set_game_name(self, name):
		self.game_name = name
	def set_weight(self, weight):
		self.weight = weight

class codeseq(mca2obj):
	'parent class for all bytecode sequences'
	def __init__(self, name):
		super(codeseq, self).__init__(name)
		self.code = []	# holds lines for assembler
		self.indents = 2
	def change_indent(self, n):
		self.indents += n
	# actually do something:
	def add_label(self, line):
		self.code.append(line)
	def add_code(self, line):
		self.code.append(self.indents * '\t' + line)

class itemdesc(codeseq):
	'code to output item description'
	def label(self):
		return 'itde_' + self.name
	# setters:
	def set_dir(self, dir, target):
		# this returns whether direction was already possible
		self.code.append(self.indents * '\t' + '+' + dir + ' ' + target.label())
		return False	# items do not have "directions" like locations
	def output(self):
		print self.label()
		for line in self.code:
			print line
		print self.indents * '\t' + '+end_itemdesc'

class procedure(codeseq):
	'callable code'
	def label(self):
		return 'proc_' + self.name
	# setters:
	def set_dir(self, dir, target):
		# this returns whether direction was already possible
		self.code.append(self.indents * '\t' + '+' + dir + ' ' + target.label())
		return False	# procedures do not have "directions" like locations
	def output(self):
		print self.label()
		for line in self.code:
			print line
		print self.indents * '\t' + '+end_procedure'

class use(codeseq):
	'code to execute when player enters USE A'
	def __init__(self, name):
		super(use, self).__init__(name)
		self.hinz = None
	# setters
	def set_item(self, hinz):
		self.hinz = hinz
	def output(self):
		print '\t!wo +\t; link pointer'
		print '\t!by ' + self.hinz.offset_name()
		for line in self.code:
			print line
		print self.indents * '\t' + '+end_use'

class combi(codeseq):
	'code to execute when player enters COMBINE A WITH B'
	def __init__(self, name):
		super(combi, self).__init__(name)
		self.hinz = None
		self.kunz = None
	# setters
	def set_items(self, hinz, kunz):
		self.hinz = hinz
		self.kunz = kunz
	def output(self):
		print '\t!wo +\t; link pointer'
		print '\t+ordered ' + self.hinz.offset_name() + ', ' + self.kunz.offset_name()
		for line in self.code:
			print line
		print self.indents * '\t' + '+end_combi'

class location(codeseq):
	'code to execute when entering a location'
	def __init__(self, name):
		super(location, self).__init__(name)
		self.extdirs = {}	# directions given via two-way feature
		self.forced_value = None	# only used for "NOWHERE" and "INVENTORY"
	def label(self):
		return 'location_' + self.name
	# setters:
	def set_dir(self, dir, target):
		# this returns whether direction was already possible
		result = dir in self.extdirs
		self.code.append(self.indents * '\t' + '+' + dir + ' ' + target.label())
		return result
	def set_extdir(self, dir, target):
		'call this for the two-way feature'
		# this returns whether direction was already possible
		result = dir in self.extdirs
		self.extdirs[dir] = target
		return result
	def set_forced_value(self, value):
		self.forced_value = value
	def output(self):
		if self.forced_value != None:
			print '!addr\t' + self.label() + '\t= ' + str(self.forced_value) + '\t; pseudo location'
		else:
			print self.label()
			# stored directions are the reason this class needs to overwrite the output method:
			for dir in self.extdirs:
				print self.indents * '\t' + '+' + dir + ' ' + self.extdirs[dir].label()
			for line in self.code:
				print line
			print self.indents * '\t' + '+end_location'

class convertor(object):
	'converts MCA2 source to ACME source'
	def __init__(self):
		self.allowed_errors = 5	# convertor stops after this many errors
		self.in_comment = False	# for c-style multi-line comments
		self.text_mode = False	# needed to add command prefix and trailing NUL char
		self.codeseq = None	# needed to track locations/procedures/combinations/usages
		self.cond_state = [0]	# keeps track of "if/elif/else/endif" and nesting
		self.code = []	# for stuff from "asm" lines
		self.subst = dict()	# dictionary for "define/enum" substitutions
		self.stringcoll = stringcoll()
		self.line_of_def = dict()	# object name to line of definition
		# special dictionaries with constructor for new entries
		self.procedures = mydict(procedure)	# procedures
		self.locations = mydict(location)	# locations
		self.uses = mydict(use)		# usages ("use A")
		self.combis = mydict(combi)		# combinations ("combine A with B")
		self.items = mydict(item)	# items player can interact with
		self.vars = mydict(symbol)	# game variables
		self.fakevars = mydict(symbol)	# constant values (used in comparisons and assignments), handled as if game vars
		# make sure "start" location is marked as referenced to inhibit confusing error
		start = self.get_object(self.locations, 'start')
		self.get_object(self.procedures, 'intro')
		# create some reserved names:
		# special value for lines below
		self.line_number = '<predefined>'
		# create pseudo item "PLAYER"
		PLAYER_item = self.get_object(self.items, 'PLAYER', define=True)
		PLAYER_item.reference()	# suppress warning if never referenced
		PLAYER_item.set_game_name('nullstring')
		PLAYER_item.set_weight('$80')	# make sure player cannot put player into inventory ;)
		PLAYER_item.set_default(start.label())
		# create pseudo location "NOWHERE" to be able to hide items and disable directions
		NOWHERE_location = self.get_object(self.locations, 'NOWHERE', define=True)
		NOWHERE_location.reference()	# suppress warning if never referenced
		NOWHERE_location.set_forced_value(0)
		# create pseudo location "INVENTORY" where items can be moved
		INVENTORY_location = self.get_object(self.locations, 'INVENTORY', define=True)
		INVENTORY_location.reference()	# suppress warning if never referenced
		INVENTORY_location.set_forced_value(1)
		# create pseudo var "__TMP__" for holding literal
		TMP_var = self.get_object(self.vars, '__TMP__', define=True)
		TMP_var.reference()	# suppress warning if never referenced
		TMP_var.set_default(0)
		# correct start value for later
		self.line_number = 0
	def error(self, msg):
		message('Error: ' + msg)
		if self.allowed_errors == 0:
			sys.exit(1)
		self.allowed_errors -= 1
	def warning_line(self, msg):
		warning('in line %d: %s!' % (self.line_number, msg))
	def error_line(self, msg):
		self.error('in line %d: %s!' % (self.line_number, msg))
	#def err_serious_line(self, msg):
	#	print >> sys.stderr, 'Serious error in line %d: %s!' % (self.line_number, msg)
	#	sys.exit(1)
	def get_object(self, dict, name, define = False):
		'get const/var/procedure/location/whatever by name. if it does not exist, create'
		'if "define" is given, store current line number.'
		'otherwise, set "referenced" to True.'
		name = nospace(name)	# remove spaces before/after
		if name in dict:
			obj = dict[name]	# use existing
			just_created = False
		else:
			obj = dict.constructor(name)	# create new
			dict[name] = obj	# and store
			just_created = True
		if define:
			if name in self.line_of_def:
				self.error_line('Object "' + name + '" has already been defined in line ' + self.line_of_def[name])
			else:
				self.line_of_def[name] = str(self.line_number)
				dict.define(obj)
		else:
			obj.reference()
			if just_created:
				dict.reference(obj)
		return obj

	def add_location_direction(self, direction, target_name):
		# add direction possibility to current location
		target_location = self.get_object(self.locations, target_name)
		if self.codeseq.set_dir(direction, target_location):
			self.warning_line('Direction "' + direction + '" was already set')
	def add_location_backdirection(self, target_name, direction):
		# add current location as direction possibility to other location
		target_location = self.get_object(self.locations, target_name)
		self.codeseq.reference()
		if target_location.set_extdir(direction, self.codeseq):
			self.warning_line('Direction "' + direction + '" was already set')
	def get_value(self, string):
		'return value of number literal'
		try:
			num = int(string)
		except:
			self.error_line('Cannot determine numerical value of "' + string + '"')
			num = 0	# make sure script does not crash
		return num
	def get_force2var(self, string):
		'convert literal/var name string to var object'
		string = nospace(string)
		if string in self.vars:
			self.vars[string].reference()
			return self.vars[string]	# return var object
		# if no var, must be literal - convert to number strings
		value = self.get_value(string)
		fakevar = self.get_object(self.fakevars, str(value))
		fakevar.set_default(value)
		return fakevar
	def add_code(self, line):
		self.code.append('\t' + line)
	def check_refs(self, dict, name):
		for thing in dict.get_undefd_and_refd():
			self.error(name + ' referenced but not defined: ' + thing.name)
			#if loc.line_of_def and not loc.referenced:
			#	warning('location "' + loc.name + '" defined but never used')
			#if loc.referenced and not loc.line_of_def:
			#	self.error('location "' + loc.name + '" referenced but not defined')
	def output(self):
		self.check_refs(self.items, 'item')
		self.check_refs(self.vars, 'variable')
		self.check_refs(self.procedures, 'procedure')
		self.check_refs(self.locations, 'location')
		print ';ACME 0.96.2'
		print ';'
		print '; DO NOT EDIT THIS FILE! THIS FILE IS AUTOMATICALLY GENERATED!'
		print ';'

		# symbol definitions are given first:

		print '; stuff generated by "asm" lines:'
		for line in self.code:
			print line
		print

		var_index = 0
		print '; var offsets:'
		print '\t; items:'
		for item in self.items.get_defined():	# use unref'd items as well, they might be red herrings
			print '\t' + item.offset_name() + '\t= ' + str(var_index) + '\t; default value is', item.default
			var_index += 1
		print '\tgamevars_ITEMCOUNT\t=', var_index	# == len(self.items)
		print '\t; game vars:'
		for var in self.vars.get_defd_and_refd():
			# FIXME - compare "referenced vars" to actual list!
			print '\t' + var.offset_name() + '\t= ' + str(var_index) + '\t; default value is', var.default
			var_index += 1

		print '\tgamevars_SAVECOUNT\t=', var_index	# == len(self.items) + len(self.vars)
		print '\t; fake vars (literals):'
		for fakevar in self.fakevars.get_referenced():
			print '\t' + fakevar.offset_name() + '\t= ' + str(var_index)
			var_index += 1
		print '\tgamevars_COUNT\t=', var_index	# == len(self.items) + len(self.vars) + len(self.fakevars)
		print

		# all data tables are put into macro so backend can put where needed:

		print '!macro game_tables {'
		print

		items_defaults = [str(item.default) for item in self.items.get_defined()]	# use unref'd items as well, they might be red herrings
		vars_defaults = [str(symbol.default) for symbol in self.vars.get_defd_and_refd()]
		fakevars_defaults = [str(symbol.default) for symbol in self.fakevars.get_referenced()]
		print 'gamevars_defaults_lo'
		print '\t!by <' + ', <'.join(items_defaults) + '\t; items'
		print '\t!by <' + ', <'.join(vars_defaults) + '\t; variables'
		if len(fakevars_defaults):
			print '\t!by <' + ', <'.join(fakevars_defaults) + '\t; literals'
		print 'gamevars_defaults_hi'
		print '\t!by >' + ', >'.join(items_defaults) + '\t; items'
		print '\t!by >' + ', >'.join(vars_defaults) + '\t; variables'
		if len(fakevars_defaults):
			print '\t!by >' + ', >'.join(fakevars_defaults) + '\t; literals'
		print

		# item weights
		print '; item weights:'
		items_weights = [item.weight for item in self.items.get_defined()]	# use unref'd items as well, they might be red herrings
		print 'item_weight\t!by ' + ', '.join(items_weights)
		print

		# pointer arrays and actual strings
		print '; string pointers:'
		items_names = [item.game_name for item in self.items.get_defined()]	# use unref'd items as well, they might be red herrings
		print 'item_name_lo\t!by <' + ', <'.join(items_names)
		print 'item_name_hi\t!by >' + ', >'.join(items_names)
		print '; strings:'
		for label, string in self.stringcoll.get_all():
			print label + '\t!tx ' + string + ', 0'
		print

		# item description pointers
		print '; item description pointers:'
		items_descs = [item.description.label() for item in self.items.get_defined()]	# use unref'd items as well, they might be red herrings
		print 'item_desc_lo\t!by <' + ', <'.join(items_descs)
		print 'item_desc_hi\t!by >' + ', >'.join(items_descs)
		# FIXME - solve weight/size issue: split items into two groups to get rid of lookup table?
		# FIXME - in future, iterate over items twice and do mobile/fixed items separately?
		print

		print '; item descriptions:'
		for item in self.items.get_defined():	# use unref'd items as well, they might be red herrings
			item.description.output()
			print

		print '; usages:'
		print 'uses'
		for use in self.uses.get_defined():
			use.output()
			print '+'
		print '\t!wo 0\t; end marker'
		print
		print '; combinations:'
		print 'combis'
		for combi in self.combis.get_defined():
			combi.output()
			print '+'
		print 'nullstring\t!wo 0\t; end marker (doubles as "nullstring" terminator)'
		print
		print '; procedures:'
		for proc in self.procedures.get_defd_and_refd():
			proc.output()
			print
		print '; locations:'
		for loc in self.locations.get_defd_and_refd():
			loc.output()
			print
		print '; end of actual data'
		print
		print '} ; end of macro'
		print '!eof'
		#print 'debugging info:'
		print '; end of auto-generated file'
# helper functions to parse lines:
	def preprocess(self, line_in):
		'count and remove indentation characters, remove comments'
		indents = 1	# leading prefix for binary space/tab bit pattern
		count_indents = True
		quotes = None
		line_out = ['']
		for char in line_in:
			# count indentation
			if count_indents:
				if char == ' ':
					indents <<= 1	# append 0 bit
					continue;
				elif char == '\t':
					indents = (indents << 1) + 1	# append 1 bit
					continue;
				else:
					count_indents = False
			# do not change anything inside strings:
			if quotes != None:
				# we're inside quotes, so check for end of quotes:
				if char == quotes:
					quotes = None	# found end of quotes
				line_out[-1] += char
				continue
			# we're not inside quotes, so check for quotes:
			if char == '"' or char == "'":
				quotes = char
				line_out[-1] += char
				continue	# do not remove '#' in strings
			# check for comments:
			if char == '#':
				break	# remove comment
			# separator?
			if char == ' ' or char == '\t':
				if line_out[-1] != '':
					line_out.append('')
				continue
			line_out[-1] += char
		if quotes != None:
			self.error_line('quotes still open at end of line')
		if line_out[-1] == '':
			line_out = line_out[:-1]
		# subst
		for idx in range(0, len(line_out)):
			if line_out[idx] in self.subst:
				line_out[idx] = self.subst[line_out[idx]]
		return indents, line_out
	def get_args(self, line, howmany):
		'ensure correct number of args and return them'
		if len(line) < 1 + howmany:
			self.error_line('Too few arguments for keyword')
		elif len(line) > 1 + howmany:
			self.error_line('Too many arguments for keyword')
		return line[1:(1 + howmany)]
# helper functions to close logical blocks:
	def no_text(self):
		'if we are in text mode, terminate'
		if self.text_mode:
			self.codeseq.add_code('+terminate')
			self.text_mode = False
	def new_code(self):
		'if we are in description/location/procedure/usage/combination, terminate'
		self.no_text()
		if self.codeseq != None:
			if self.cond_state != [0]:
				self.error_line('cannot start new description/location/procedure/usage/combination, there are "if" blocks left open')
			self.codeseq = None
# functions to parse different line types:
	def process_asm_line(self, line):
		'line to pass to assembler unchanged'
		if self.codeseq != None:
			self.error_line('Please put "asm" lines before all items/locations/procedures/usages/combinations')
		self.add_code(' '.join(line[1:]))
	def process_text_line(self, line):
		'text line'
		if self.text_mode == False:
			self.codeseq.add_code('+print')
			self.text_mode = True
		self.codeseq.add_code('!tx ' + ' '.join(line))
	def process_code_line(self, dict, name):
		self.new_code()	# close previous code sequence, if there was one
		# check
		obj = self.get_object(dict, name, define=True)	# create
		# make current
		self.codeseq = obj
		return obj
	def process_use_line(self, line):
		'code to call if player wants to use item'
		item = self.get_args(line, 1)[0]
		item = self.get_object(self.items, item)
		use = self.process_code_line(self.uses, str(id(item)))
		use.set_item(item)
	def process_combi_line(self, line):
		'code to call if player wants to combine items'
		item1, item2 = self.get_args(line, 2)
		item1 = self.get_object(self.items, item1)
		item2 = self.get_object(self.items, item2)
		combi = self.process_code_line(self.combis, str(id(item1)) + '_' + str(id(item2)))
		combi.set_items(item1, item2)
	def process_proc_loc_line(self, line, dict):
		'new procedure or location'
		name = self.get_args(line, 1)[0]
		self.process_code_line(dict, name)
	def process_callproc_line(self, line):
		'call procedure'
		self.no_text()
		proc_name = self.get_args(line, 1)[0]
		proc = self.get_object(self.procedures, proc_name)
		self.codeseq.add_code('+gosub ' + proc.label())
	def process_callasm_line(self, line):
		'call machine language'
		self.no_text()
		asm_name = self.get_args(line, 1)[0]
		self.codeseq.add_code('+callasm ' + asm_name)
	def process_dir_line(self, direction, line, backdir=None):
		'allow a direction of movement and specify target, with two-way option'
		self.no_text()
		target_loc_name = self.get_args(line, 1)[0]
		self.add_location_direction(direction, target_loc_name)
		if backdir:
			if self.cond_state != [0]:
				self.error_line('two-way directions cannot be used in "if" blocks')
			else:
				self.add_location_backdirection(target_loc_name, backdir)
	def process_dirs_line(self, dir1, dir2, line, two_way=False):
		'allow two directions of movement and specify targets, with two-way option'
		self.no_text()
		target_loc_name1, target_loc_name2 = self.get_args(line, 2)
		self.add_location_direction(dir1, target_loc_name1)
		self.add_location_direction(dir2, target_loc_name2)
		if two_way:
			if self.cond_state != [0]:
				self.error_line('two-way directions cannot be used in "if" blocks')
			else:
				self.add_location_backdirection(target_loc_name1, dir2)
				self.add_location_backdirection(target_loc_name2, dir1)
	def add_substitution(self, name, value):
		'helper function for "define" and "enum" lines'
		if name in self.line_of_def:
			self.error_line('Name "' + name + '" has already been assigned to an object in line ' + self.line_of_def[name])
		else:
			self.subst[name] = value
	def process_define_line(self, line):
		'definition for text substitution (basically symbolic constants)'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		name, value = self.get_args(line, 2)
		self.add_substitution(name, value)
	def process_enum_line(self, line):
		'enumerate symbolic constants'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		value = 0
		for word in line[1:]:	# remove 'enum' keyword, line is already split at spaces
			self.add_substitution(word, str(value))
			value += 1
	def process_var_line(self, line):
		'variable declaration'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		name, start_value = self.get_args(line, 2)
		var = self.get_object(self.vars, name, define=True)
		# get actual number for start value
		num = self.get_value(start_value)
		var.set_default(num)
	def process_item_line(self, line):
		'declare item for player to interact with'
		self.new_code()	# close previous code sequence, if there was one
		weight, location, name, game_name = self.get_args(line, 4)
		location = self.get_object(self.locations, location).label()
		item = self.get_object(self.items, name, define=True)
		game_name = self.stringcoll.add(game_name)
		if weight == 'small':
			item.set_weight('0')
		elif weight == 'large':
			item.set_weight('$80')
		else:
			self.error_line('Item size must be "small" or "large"')
		item.set_default(location)
		item.set_game_name(game_name)
		# make current
		self.codeseq = item.description
	def process_delay_line(self, line):
		'wait for given number of .1 seconds'
		self.no_text()
		var = self.get_force2var(self.get_args(line, 1)[0])	# arg could be var or const or literal
		self.codeseq.add_code('+delay ' + var.offset_name())
# if/elif/else/endif helpers:
	def process_condition(self, line):
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
		if op.endswith('@'):
			'args are expected to be ITEM/ITEM or ITEM/LOCATION'
			var1 = self.get_object(self.items, hinz)
			if kunz in self.items:
				var2 = self.get_object(self.items, kunz)
			else:
				loc = self.get_object(self.locations, kunz)
				var2 = self.get_object(self.vars, '__TMP__')
				self.codeseq.add_code('+varloadimm ' + var2.offset_name() + ', ' + loc.label())
		else:
			var1 = self.get_force2var(hinz)
			var2 = self.get_force2var(kunz)
		code = '+if_' + oper + ' ' + var1.offset_name() + ', ' + var2.offset_name()
		self.codeseq.add_code(code + ', .c_after' + str(self.cond_state[-1]))
	def end_cond_block(self):
		self.codeseq.add_code('+goto .c_end')
		self.codeseq.add_label('.c_after' + str(self.cond_state[-1]))
# if/elif/else/endif:
	def process_if_line(self, line):
		self.no_text()
		self.codeseq.add_code('!zone {')
		self.cond_state.append(1)	# go deeper, then in 1st block of if/elif/else/endif
		self.process_condition(line)
		self.codeseq.change_indent(1)
	def process_elif_line(self, line):
		self.no_text()
		if self.cond_state[-1] == 0:
			self.error_line('Used ELIF without IF')
		if self.cond_state[-1] == -1:
			self.error_line('Used ELIF after ELSE')
		self.end_cond_block()
		self.cond_state[-1] += 1	# in next block of if/elif/else/endif
		self.codeseq.change_indent(-1)
		self.process_condition(line)
		self.codeseq.change_indent(1)
	def process_else_line(self, line):
		self.no_text()
		if ' '.join(line) != 'else':
			self.error_line('Garbage after ELSE?!')
		if self.cond_state[-1] == 0:
			self.error_line('Used ELSE without IF')
		if self.cond_state[-1] == -1:
			self.error_line('Used ELSE after ELSE')
		self.end_cond_block()
		self.codeseq.change_indent(-1)
		self.codeseq.add_code(';else')
		self.codeseq.change_indent(1)
		self.cond_state[-1] = -1	# in ELSE block of if/elif/else/endif
	def process_endif_line(self, line):
		self.no_text()
		if ' '.join(line) != 'endif':
			self.error_line('Garbage after ENDIF?!')
		if self.cond_state[-1] == 0:
			self.error_line('Used ENDIF without IF')
		if self.cond_state[-1] != -1:
			self.codeseq.add_label('.c_after' + str(self.cond_state[-1]))
		self.codeseq.add_label('.c_end')
		self.cond_state.pop()	# leave nesting level
		self.codeseq.change_indent(-1)
		self.codeseq.add_code('} ; end of zone')
# var changing:
	def process_move_line(self, line):
		'move an item to a different location'
		self.no_text()
		item, target = self.get_args(line, 2)
		item = self.get_object(self.items, item)
		if target in self.items:
			itemsrc = self.get_object(self.items, target)
			self.codeseq.add_code('+varcopy ' + item.offset_name() + ', ' + itemsrc.offset_name())
		else:
		#elif target in self.locations:
			location = self.get_object(self.locations, target)
			# FIXME - check for "large" item and "INVENTORY" target and complain?
			# but still the problem remains if moving large item @ small item in INV!
			self.codeseq.add_code('+varloadimm ' + item.offset_name() + ', ' + location.label())
		#else:
		#	self.error_line('Target is neither location nor item')
	def process_gain_line(self, line):
		'move an item to INVENTORY'
		item = self.get_args(line, 1)[0]
		self.process_move_line(['move', item, 'INVENTORY'])
	def process_hide_line(self, line):
		'move an item to NOWHERE'
		item = self.get_args(line, 1)[0]
		self.process_move_line(['move', item, 'NOWHERE'])
	def process_let_line(self, line):
		'writing to variable'
		self.no_text()
		# arg checking was done by caller, to be able to recognize this type of line...
		target_var = self.get_object(self.vars, nospace(line[0]))
		# FIXME - make sure target var is not read-only!
		source_var = self.get_force2var(line[2])
		self.codeseq.add_code('+varcopy ' + target_var.offset_name() + ', ' + source_var.offset_name())
	def process_incdec_line(self, what, line):
		'increment/decrement variable'
		self.no_text()
		var = self.get_object(self.vars, self.get_args(line, 1)[0])
		# FIXME - make sure var is not read-only!
		self.codeseq.add_code('+' + what + ' ' + var.offset_name())
# outer stuff:
	def process_line(self, line):
		'process a single line of input'
		self.line_number += 1
		indents, line = self.preprocess(line)
		#print indents, line
		#return
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
			# everything else should start with a keyword...
			key = line[0]
			if key == 'asm':
				self.process_asm_line(line)
			elif key == 'define':
				self.process_define_line(line)
			elif key == 'enum':
				self.process_enum_line(line)
			elif key == 'var':
				self.process_var_line(line)
			elif key == 'inc':
				self.process_incdec_line('varinc', line)
			elif key == 'dec':
				self.process_incdec_line('vardec', line)
			elif key == 'item':
				self.process_item_line(line)
			elif key == 'move':
				self.process_move_line(line)
			elif key == 'gain':
				self.process_gain_line(line)
			elif key == 'hide':
				self.process_hide_line(line)
			elif key == 'delay':
				self.process_delay_line(line)
			elif key == 'if':
				self.process_if_line(line)
			elif key == 'elif':
				self.process_elif_line(line)
			elif key == 'else':
				self.process_else_line(line)
			elif key == 'endif':
				self.process_endif_line(line)
			elif key == 'loc':
				self.process_proc_loc_line(line, self.locations)
			elif key == 'use':
				self.process_use_line(line)
			elif key == 'combine':
				self.process_combi_line(line)
			elif key == 'using':	# older form of "combine"
				self.process_combi_line(line)
			elif key == 'proc':
				self.process_proc_loc_line(line, self.procedures)
			elif key == 'callproc':
				self.process_callproc_line(line)
			elif key == 'callasm':
				self.process_callasm_line(line)
			elif key == 'n':
				self.process_dir_line('north', line)
			elif key == 'n2':
				self.process_dir_line('north', line, 'south')
			elif key == 's':
				self.process_dir_line('south', line)
			elif key == 's2':
				self.process_dir_line('south', line, 'north')
			elif key == 'ns':
				self.process_dirs_line('north', 'south', line)
			elif key == 'ns2':
				self.process_dirs_line('north', 'south', line, two_way=True)
			elif key == 'w':
				self.process_dir_line('west', line)
			elif key == 'w2':
				self.process_dir_line('west', line, 'east')
			elif key == 'e':
				self.process_dir_line('east', line)
			elif key == 'e2':
				self.process_dir_line('east', line, 'west')
			elif key == 'we':
				self.process_dirs_line('west', 'east', line)
			elif key == 'we2':
				self.process_dirs_line('west', 'east', line, two_way=True)
			elif key == 'u':
				self.process_dir_line('up', line)
			elif key == 'u2':
				self.process_dir_line('up', line, 'down')
			elif key == 'd':
				self.process_dir_line('down', line)
			elif key == 'd2':
				self.process_dir_line('down', line, 'up')
			elif key == 'ud':
				self.process_dirs_line('up', 'down', line)
			elif key == 'ud2':
				self.process_dirs_line('up', 'down', line, two_way=True)
			elif len(line) == 3 and line[1] == '=':
				# ...or is an assignment to a variable
				self.process_let_line(line)
			else:
				self.error_line('Line type not recognised')
		#debug:
		#self.codeseq.code.append(str(indents) + line)

	def parse_file(self, filename):
		with open(filename, 'r') as file:
			for line in file:
				if len(line):
					if line[-1] == '\n':
						line = line[:-1]
				if len(line):
					if line[-1] == '\r':
						line = line[:-1]
				self.process_line(line)
			self.new_code()	# make sure last text/code sequence is terminated

def main():
	if len(sys.argv) != 2:
		print >> sys.stderr, 'Error: wrong number of arguments'
		sys.exit(1)
	source_file = sys.argv[1]
	conv = convertor()
	conv.parse_file(source_file)
	conv.output()

if __name__ == '__main__':
	main()

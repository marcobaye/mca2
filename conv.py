#!/usr/bin/python2
import sys

operators = [
	['==', 'equal'],
	['!=', 'not_equal'],
	['<=', 'smaller_or_equal'],	# these longer
	['>=', 'greater_or_equal'],	# strings must
	['<', 'smaller'],	# be in list before these
	['>', 'greater']	# shorter ones!
]
# FIXME - add "@" and "!@" for "item at location" and "item not at location"

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

class mca2obj(object):
	'parent class for everything defined in game description file'
	def __init__(self, name):
		self.name = name	# symbolic name
		self.line_of_def = None	# line number of definition (for "already defined" error)
		self.referenced = False	# for debugging output ("object XYZ never used!)
	def reference(self):
		self.referenced = True

class symbol(mca2obj):
	'parent class for const, item, var and fakevar'
	def __init__(self, name):
		super(symbol, self).__init__(name)
		self.default = None	# default value at start of game
		self.readonly = False	# currently only "HERE" is made read-only
	def offset_name(self):
		return 'vo_' + self.name
	def set_default(self, value):
		self.default = value
	def make_readonly(self):
		self.readonly = True

class item(symbol):
	'game item player can interact with'
	def __init__(self, name):
		super(item, self).__init__(name)
		self.game_name = None
		self.description = None
		self.weight = 0
	def set_game_name(self, name):
		self.game_name = name
	def set_description(self, desc):
		self.description = desc
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
	def output(self):
		print self.label()
		for line in self.code:
			print line
		print self.indents * '\t' + '+end_procedure'

class procedure(codeseq):
	'callable code'
	def label(self):
		return 'proc_' + self.name
	# setters:
	def set_dir(self, dir, target):
		# this returns whether direction was already possible
		self.code.append(self.indents * '\t' + '+' + dir + ' ' + target.label())
		return False	# procedures do not have "directions" like locations

class usage(codeseq):
	'code to execute when player enters USE A WITH B'
	def __init__(self, name, hinz, kunz):
		super(usage, self).__init__(name)
		self.hinz = hinz
		self.kunz = kunz
	def label(self):
		return 'usage_' + self.hinz + '_' + self.kunz

class location(codeseq):
	'code to execute when entering a location'
	def __init__(self, name):
		super(location, self).__init__(name)
		self.extdirs = {}	# directions given via two-way feature
		self.forced_value = None	# only used for "OFF" and "INVENTORY"
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
			print "!addr\t" + self.label() + " = " + str(self.forced_value) + "\t; pseudo location"
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
		self.codeseq = None	# needed to track locations/procedures/usages
		self.cond_state = [0]	# keeps track of "if/elif/else/endif" and nesting
		self.code = []	# for stuff from "asm" lines
		# special dictionaries with constructor for new entries
		self.procedures = mydict(procedure)	# procedures
		self.locations = mydict(location)	# locations
		self.usages = mydict(usage)		# usages ("use A with B")
		self.consts = mydict(symbol)	# holds symbolic constants
		self.items = mydict(item)	# items player can interact with
		self.vars = mydict(symbol)	# game variables
		self.fakevars = mydict(symbol)	# constant values (used in comparisons and assignments), handled as if game vars
		# make sure "start" location is marked as referenced to inhibit confusing error
		start = self.get_object(self.locations, 'start')
		# create some reserved names:
		# special value for lines below
		self.line_number = '<predefined>'
		# create pseudo location "NOWHERE" to be able to hide items and disable directions
		NOWHERE_location = self.get_object(self.locations, 'NOWHERE', define=True)
		NOWHERE_location.reference()	# suppress warning if never referenced
		NOWHERE_location.set_forced_value(0)
		# create pseudo location "INVENTORY" where items can be moved
		INVENTORY_location = self.get_object(self.locations, 'INVENTORY', define=True)
		INVENTORY_location.reference()	# suppress warning if never referenced
		INVENTORY_location.set_forced_value(1)
		# create pseudo var "HERE" to be able to determine current location
		HERE_var = self.get_object(self.vars, 'HERE', define=True)
		HERE_var.reference()	# suppress warning if never referenced
		HERE_var.set_default(start.label())
		HERE_var.make_readonly()
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
		else:
			obj = dict.constructor(name)	# create new
			dict[name] = obj	# and store
		if define:
			if obj.line_of_def:
				self.error_line('Object "' + name + '" has already been defined in line ' + obj.line_of_def)
			else:
				obj.line_of_def = str(self.line_number)
		else:
			obj.reference()
		return obj

	def add_location_direction(self, direction, target_name):
		# add direction possibility to current location
		target_location = self.get_object(self.locations, target_name)
		target_location.referenced = True
		if self.codeseq.set_dir(direction, target_location):
			self.warning_line('Direction "' + direction + '" was already set')
	def add_location_backdirection(self, target_name, direction):
		# add current location as direction possibility to other location
		target_location = self.get_object(self.locations, target_name)
		self.codeseq.referenced = True
		if target_location.set_extdir(direction, self.codeseq):
			self.warning_line('Direction "' + direction + '" was already set')
	def get_value(self, string):
		'return value of number literal or symbolic constant'
		if string in self.consts:
			return self.consts[string].default
		try:
			num = int(string)
		except:
			self.error_line('Cannot determine numerical value of "' + string + '"')
			num = 0	# make sure script does not crash
		return num
	def get_force2var(self, string):
		'convert literal/const/var name string to var object'
		string = nospace(string)
		if string in self.vars:
			return self.vars[string]	# return var object
		# const names are converted to number strings
		value = self.get_value(string)
		fakevar = self.get_object(self.fakevars, str(value))
		fakevar.set_default(value)
		return fakevar
	def add_code(self, line):
		self.code.append('\t' + line)
	def output(self):
		print ';ACME 0.96.2'
		print ';'
		print '; DO NOT EDIT THIS FILE! THIS FILE IS AUTOMATICALLY GENERATED!'
		print ';'
		print '!macro autogenerated {'
		# FIXME - prune dicts by removing all unreferenced entries?
		items_defaults = [str(symbol.default) for symbol in self.items.values()]
		vars_defaults = [str(symbol.default) for symbol in self.vars.values()]
		fakevars_defaults = [str(symbol.default) for symbol in self.fakevars.values()]
		print 'gamevars_defaults_lo'
		if len(items_defaults):
			print '\t!by <' + ', <'.join(items_defaults) + '\t; items'
		print '\t!by <' + ', <'.join(vars_defaults) + '\t; variables'
		print '\t!by <' + ', <'.join(fakevars_defaults) + '\t; literals'
		print 'gamevars_defaults_hi'
		if len(items_defaults):
			print '\t!by >' + ', >'.join(items_defaults) + '\t; items'
		print '\t!by >' + ', >'.join(vars_defaults) + '\t; variables'
		print '\t!by >' + ', >'.join(fakevars_defaults) + '\t; literals'
		var_index = 0
		print '; var offsets:'
		print '\t; items:'
		# FIXME - in future, iterate over items twice and do mobile/fixed items separately!
		for i in self.items:
			print type(i)
			print '\t' + self.items[i].offset_name() + '\t= ' + str(var_index) + '\t; default value is', self.items[i].default
			var_index += 1
		print '\tgamevars_ITEMCOUNT\t=', var_index	# == len(self.items)
		print '\t; game vars:'
		for v in self.vars:
			# FIXME - compare "referenced vars" to actual list!
			print '\t' + self.vars[v].offset_name() + '\t= ' + str(var_index) + '\t; default value is', self.vars[v].default
			var_index += 1
		print '\tgamevars_SAVECOUNT\t=', var_index	# == len(self.items) + len(self.vars)
		print '\t; fake vars (literals):'
		for f in self.fakevars:
			print '\t' + self.fakevars[f].offset_name() + '\t= ' + str(var_index)
			var_index += 1
		print '\tgamevars_COUNT\t=', var_index	# == len(self.items) + len(self.vars) + len(self.fakevars)
		print
		print '; stuff generated by "asm" lines:'
		for line in self.code:
			print line
		print
		print '; procedures:'
		for proc in self.procedures:
			self.procedures[proc].output()
		print
		print '; locations:'
		for loc in self.locations:
			loc = self.locations[loc]
			if loc.line_of_def and not loc.referenced:
				warning('location "' + loc.name + '" defined but never used')
			if loc.referenced and not loc.line_of_def:
				self.error('location "' + loc.name + '" referenced but not defined')
			loc.output()
		print
		print '; usages:'
		for usage in self.usages:
			self.usages[usage].output()
		print
		print '; end of actual data'
		print '} ; end of macro'
		print '!eof'
		#print 'debugging info:'
		print '; end of auto-generated file'
# helper functions to parse lines:
	def preprocess(self, line_in):
		'count and remove indentation characters, remove comments'
		indents = 1	# leading prefix for binary space/tab pattern
		count_indents = True
		quotes = None
		line_out = ''
		for char in line_in:
			# count indentation
			if count_indents:
				if char == ' ':
					indents <<= 1
					continue;
				elif char == '\t':
					indents = (indents << 1) + 1
					continue;
				else:
					count_indents = False
			# do not change anything inside strings:
			if quotes != None:
				# we're inside quotes, so check for end of quotes:
				if char == quotes:
					quotes = None	# found end of quotes
				line_out += char
				continue
			# we're not inside quotes, so check for quotes:
			if char == '"' or char == "'":
				quotes = char
				line_out += char
				continue	# do not remove '#' in strings
			# check for comments:
			if char == '#':
				break	# remove comment
			line_out += char
		if quotes != None:
			self.error_line('quotes still open at end of line')
		return indents, line_out
	def get2of2(self, line):
		'make sure line consists of two parts and return second one'
		parts = line.split()
		if len(parts) != 2:
			self.error_line('line does not fit "KEYWORD ARGUMENT" format')
		return parts[1]
	def get2and3of3(self, line):
		'make sure line consists of three parts and return second and third'
		parts = line.split()
		if len(parts) != 3:
			self.error_line('line does not fit "KEYWORD ARG1 ARG2" format')
		return parts[1], parts[2]
# helper functions to close logical blocks:
	def no_text(self):
		'if we are in text mode, terminate'
		if self.text_mode:
			self.codeseq.add_code('+terminate')
			self.text_mode = False
	def new_code(self):
		'if we are in location/procedure/usage, terminate'
		if self.codeseq != None:
			if self.cond_state != [0]:
				self.error_line('cannot start new location/procedure/usage, there are "if" blocks left open')
			self.codeseq = None
# functions to parse different line types:
	def process_asm_line(self, line):
		'line to pass to assembler unchanged'
		if self.codeseq != None:
			self.error_line('Please put "asm" lines before all locations/procedures/usages')
		self.add_code(line[4:])
	def process_text_line(self, line):
		'text line'
		if self.text_mode == False:
			self.codeseq.add_code('+print')
			self.text_mode = True
		self.codeseq.add_code('!tx ' + line)
	def process_defproc_loc_line(self, line, dict):
		'new procedure or location'
		self.no_text()
		self.new_code()	# close previous code sequence, if there was one
		# check
		name = self.get2of2(line)
		obj = self.get_object(dict, name, define=True)	# create
		# make current
		self.codeseq = obj
	def process_callproc_line(self, line):
		'call procedure'
		self.no_text()
		proc_name = self.get2of2(line)
		proc = self.get_object(self.procedures, proc_name)
		self.codeseq.add_code('+gosub ' + proc.label())
	def process_callasm_line(self, line):
		'call machine language'
		self.no_text()
		asm_name = self.get2of2(line)
		self.codeseq.add_code('+callasm ' + asm_name)
	def process_dir_line(self, direction, line, backdir=None):
		'allow a direction of movement and specify target, with two-way option'
		self.no_text()
		target_loc_name = self.get2of2(line)
		self.add_location_direction(direction, target_loc_name)
		if backdir:
			if self.cond_state != [0]:
				self.error_line('two-way directions cannot be used in "if" blocks')
			else:
				self.add_location_backdirection(target_loc_name, backdir)
	def process_dirs_line(self, dir1, dir2, line, two_way=False):
		'allow two directions of movement and specify targets, with two-way option'
		self.no_text()
		target_loc_name1, target_loc_name2 = self.get2and3of3(line)
		self.add_location_direction(dir1, target_loc_name1)
		self.add_location_direction(dir2, target_loc_name2)
		if two_way:
			if self.cond_state != [0]:
				self.error_line('two-way directions cannot be used in "if" blocks')
			else:
				self.add_location_backdirection(target_loc_name1, dir2)
				self.add_location_backdirection(target_loc_name2, dir1)
	def process_const_line(self, line):
		'symbolic constant definition'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		name, value = self.get2and3of3(line)
		# FIXME - make sure there is no VAR with that name!
		const = self.get_object(self.consts, name, define=True)
		# get actual value
		num = self.get_value(value)
		const.set_default(num)
	def process_enum_line(self, line):
		'enumerate symbolic constants'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		parts = line[4:].split(',')	# remove 'enum' keyword
		val = 0
		for name in parts:
			name = name.split()[0]	# remove spaces
			# FIXME - make sure there is no VAR with that name!
			const = self.get_object(self.consts, name, define=True)
			const.set_default(val)
			val += 1
	def process_var_line(self, line):
		'variable declaration'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		name, start_value = self.get2and3of3(line)
		# FIXME - make sure there is no CONST with that name!
		var = self.get_object(self.vars, name, define=True)
		# get actual number for start value
		num = self.get_value(start_value)
		var.set_default(num)
	def process_delay_line(self, line):
		'wait for given number of .1 seconds'
		self.no_text()
		var = self.get_force2var(self.get2of2(line))	# arg could be var or const or literal
		self.codeseq.add_code('+delay ' + var.offset_name())
# if/elif/else/endif helpers:
	def process_condition(self, line):
		for cmp in operators:
			if cmp[0] in line:
				break
		else:
			self.error_line('Comparison not recognised')
			return
		parts = line.split(cmp[0])
		if len(parts) != 2:
			self.error_line('Error parsing comparison')
		hinz = self.get_force2var(parts[0])
		kunz = self.get_force2var(parts[1])
		self.codeseq.add_code('+if_' + cmp[1] + ' ' + hinz.offset_name() + ', ' + kunz.offset_name() + ', .c_after' + str(self.cond_state[-1]))
	def end_cond_block(self):
		self.codeseq.add_code('+goto .c_end')
		self.codeseq.add_label('.c_after' + str(self.cond_state[-1]))
# if/elif/else/endif:
	def process_if_line(self, line):
		self.no_text()
		self.codeseq.add_code('!zone {')
		self.cond_state.append(1)	# go deeper, then in 1st block of if/elif/else/endif
		self.process_condition(line[3:])	# without "if"
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
		self.process_condition(line[5:])	# without "elif"
		self.codeseq.change_indent(1)
	def process_else_line(self, line):
		self.no_text()
		if line != "else":
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
		if self.cond_state[-1] == 0:
			self.error_line('Used ENDIF without IF')
		if self.cond_state[-1] != -1:
			self.codeseq.add_label('.c_after' + str(self.cond_state[-1]))
		self.codeseq.add_label('.c_end')
		self.cond_state.pop()	# leave nesting level
		self.codeseq.change_indent(-1)
		self.codeseq.add_code('} ; end of zone')
# var changing:
	def process_let_line(self, line):
		'writing to variable'
		self.no_text()
		parts = line.split('=')
		if len(parts) != 2:
			self.error_line('Line type not recognised')
		target_var = self.get_object(self.vars, nospace(parts[0]))
		# FIXME - make sure target var is not read-only!
		source_var = self.get_force2var(parts[1])
		self.codeseq.add_code('+let ' + target_var.offset_name() + ', ' + source_var.offset_name())
	def process_incdec_line(self, what, line):
		'increment/decrement variable'
		self.no_text()
		var = self.get_object(self.vars, self.get2of2(line))
		# FIXME - make sure var is not read-only!
		self.codeseq.add_code('+' + what + ' ' + var.offset_name())
# outer stuff:
	def process_line(self, line):
		'process a single line of input'
		self.line_number += 1
		indents, line = self.preprocess(line)
		#print indents, line
		#return
		# handle end of multi-line comment:
		if self.in_comment:
			if line.startswith('*/'):
				self.in_comment = False
				line = line[2:]
			else:
				return
		# ignore empty lines
		if line == '':
			return
		if line.startswith('/*'):
			# start of multi-line comment
			self.in_comment = True
			return
		elif line.startswith('"') or line.startswith("'"):
			# text output
			self.process_text_line(line)
		else:
			# everything else should start with a keyword...
			key = line.split()[0]
			if key == 'asm':
				self.process_asm_line(line)
			elif key == 'const':
				self.process_const_line(line)
			elif key == 'enum':
				self.process_enum_line(line)
			elif key == 'var':
				self.process_var_line(line)
			elif key == 'inc':
				self.process_incdec_line('inc', line)
			elif key == 'dec':
				self.process_incdec_line('dec', line)
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
			elif key == 'sit':	# FIXME - change to "location"
				self.process_defproc_loc_line(line, self.locations)
			elif key == 'defproc':
				self.process_defproc_loc_line(line, self.procedures)
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
			else:
				# ...or is an assignment to a variable
				self.process_let_line(line)
		#debug:
		#self.codeseq.code.append(str(indents) + line)

	def parse_file(self, filename):
		with open(filename, 'r') as file:
			for line in file:
				if line[-1] == '\n':
					line = line[:-1]
				self.process_line(line)

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

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

def var_offset_label(name):	# FIXME - make var class and call its label() function!
	return 'vo_' + name

class mca2obj(object):
	'parent class for const, var, sit and maybe later sub'
	def __init__(self, name):
		self.name = name
		self.line_of_def = 0
		self.referenced = False

class situation(mca2obj):
	'collects data about a situation'
	def __init__(self, name):
		super(situation, self).__init__(name)
		self.dirs = {}
		self.code = []
		self.indents = 2
	def label(self):
		return 's_' + self.name
	# setters:
	def set_dir(self, dir, target):
		# this returns whether direction was already possible
		result = dir in self.dirs
		self.code.append(self.indents * '\t' + '+' + dir + ' ' + target.label())
		return result
	def set_extdir(self, dir, target):
		# this returns whether direction was already possible
		result = dir in self.dirs
		self.dirs[dir] = target
		return result
	def change_indent(self, n):
		self.indents += n
	# actually do something:
	def add_label(self, line):
		self.code.append(line)
	def add_code(self, line):
		self.code.append(self.indents * '\t' + line)
	def output(self):
		print self.label()
		for dir in self.dirs:
			print self.indents * '\t' + '+' + dir + ' ' + self.dirs[dir].label()
		for line in self.code:
			print line
		print self.indents * '\t' + '+end_sit'

class convertor(object):
	'converts MCA2 source to ACME source'
	def __init__(self):
		self.allowed_errors = 10	# convertor stops after this many errors
		self.line_number = 0	# for error output
		self.in_comment = False	# for c-style multi-line comments
		self.text_mode = False	# needed to add command prefix and trailing NUL char
		self.current_sit = None	# needed so no command is issued outside of situation (and to recall current sit)
		self.cond_state = [0]	# keeps track of "if/elif/else/endif" and nesting
		self.symbols = dict()	# holds line numbers of const AND var definitions
		self.consts = dict()	# holds values of symbolic constants
		# FIXME - maybe add a symbol class and then subclass consts and vars from there?
		self.vars = dict()	# holds start values of declared variables
		self.literals = set()	# fake vars (constants used in comparisons and assigments)
		self.code = []	# for stuff from "asm" lines
		self.situations = dict()	# list of situations
		start = situation("start")
		start.referenced = True
		self.situations["start"] = start
		self.new_var('current_sit', start.label())	# reserve symbol
		# FIXME - make current_sit var read-only!
	def msg(self, msg):
		print >> sys.stderr, msg
	def warning(self, msg):
		self.msg('Warning: ' + msg)
	def error(self, msg):
		self.msg('Error: ' + msg)
		if self.allowed_errors == 0:
			sys.exit(1)
		self.allowed_errors -= 1
	def warning_line(self, msg):
		self.warning('in line %d: %s!' % (self.line_number, msg))
	def error_line(self, msg):
		self.error('in line %d: %s!' % (self.line_number, msg))
	#def err_serious_line(self, msg):
	#	print >> sys.stderr, 'Serious error in line %d: %s!' % (self.line_number, msg)
	#	sys.exit(1)
	def get_sit(self, sit_name):
		'get situation by name. if it does not exist, create'
		#print sit_name
		if sit_name in self.situations:
			return self.situations[sit_name]
		sit = situation(sit_name)
		self.situations[sit_name] = sit
		return sit
	def add_sit_dir(self, direction, target_name):
		# add direction possibility to current situation
		target_sit = self.get_sit(target_name)
		target_sit.referenced = True
		if self.current_sit.set_dir(direction, target_sit):
			self.warning_line('Direction "' + direction + '" was already set')
	def add_sit_backdir(self, target_name, direction):
		# add direction possibility to other situation
		target_sit = self.get_sit(target_name)
		self.current_sit.referenced = True
		if target_sit.set_extdir(direction, self.current_sit):
			self.warning_line('Direction "' + direction + '" was already set')
	def new_symbol(self, name):
		'if symbol already defined, complain. otherwise create.'
		if name in self.symbols:
			defline = self.symbols[name]
			if defline:
				self.error_line('Symbol "' + name + '" has already been defined in line ' + str(defline))
			else:
				self.error_line('Symbol "' + name + '" has already been defined by game engine')
		self.symbols[name] = self.line_number
	def new_var(self, name, default):
		self.new_symbol(name)
		self.vars[name] = default
	def get_var(self, string):
		var_name = string.split()[0]	# remove leading/trailing spaces
		if var_name in self.vars:
			return var_name
		self.error_line('Unknown variable "' + var_name + '"')
	def get_num(self, value):
		'return value of number literal or symbolic constant'
		if value in self.consts:
			return self.consts[value]
		try:
			num = int(value)
		except:
			self.error_line('Cannot determine numerical value of "' + value + '"')
			num = 0	# make sure script does not crash
		return num
	def get_expr(self, string):
		'get name of variable or fake literal'
		string = string.split()[0]	# remove leading/trailing spaces
		if string in self.vars:
			return string
		num = self.get_num(string)
		self.literals.add(num)
		return str(num)
	def add_code(self, line):
		self.code.append('\t' + line)
	def output(self):
		print ';ACME 0.96.2'
		print ';'
		print '; DO NOT EDIT THIS FILE! THIS FILE IS AUTOMATICALLY GENERATED!'
		print ';'
		defaultvaluestrings = [str(value) for value in self.vars.values()]
		literalvaluestrings = [str(value) for value in self.literals]
		print 'gamevars_defaults_lo'
		print '\t!by <' + ', <'.join(defaultvaluestrings) + '\t; variables'
		print '\t!by <' + ', <'.join(literalvaluestrings) + '\t; literals'
		print 'gamevars_defaults_hi'
		print '\t!by >' + ', >'.join(defaultvaluestrings) + '\t; variables'
		print '\t!by >' + ', >'.join(literalvaluestrings) + '\t; literals'
		var_index = 0
		print '; var offsets:'
		for v in self.vars:
			print '\t' + var_offset_label(v) + '\t= ' + str(var_index) + '\t; default value is', self.vars[v]
			var_index += 1
		print '\tgamevars_2SAVE\t=', var_index	# == len(self.vars)
		print '\t; literals from here on:'
		for l in self.literals:
			print '\t' + var_offset_label(str(l)) + '\t= ' + str(var_index)
			var_index += 1
		print '\tgamevars_COUNT\t=', var_index	# == len(self.vars) + len(self.literals)
		print
		print '; stuff generated by "asm" lines:'
		for line in self.code:
			print line
		print
		print '; situations:'
		for sit in self.situations:
			self.situations[sit].output()
		print '; end of actual data'
		# compare defined and referenced situations:
		for sit in self.situations:
			sit = self.situations[sit]
			if sit.line_of_def and not sit.referenced:
				self.warning('situation "' + sit.name + '" defined but never used')
			if sit.referenced and sit.line_of_def == 0:
				self.error('situation "' + sit.name + '" referenced but not defined')
		# FIXME - compare "referenced vars" to actual list!
		print '!eof'
		#print 'debugging info:'
		#print 'situations:'
		#for sit in self.situations:
		#	print sit, self.situations[sit]
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
			self.current_sit.add_code('+terminate')
			self.text_mode = False
	def no_sit(self):
		'if we are in situation, terminate'
		if self.current_sit != None:
			if self.cond_state != [0]:
				self.error_line('cannot start new situation, there are "if" blocks left open')
			self.current_sit = None
# functions to parse different line types:
	def process_asm_line(self, line):
		'line to pass to assembler unchanged'
		if self.current_sit != None:
			self.error_line('Please put "asm" lines before all situations')
		self.add_code(line[4:])
	def process_text_line(self, line):
		'text line'
		if self.text_mode == False:
			self.current_sit.add_code('+print')
			self.text_mode = True
		self.current_sit.add_code('!tx ' + line)
	def process_sit_line(self, line):
		'new situation'
		self.no_text()
		self.no_sit()	# close previous sit, if there was one
		# check
		sit_name = self.get2of2(line)
		sit = self.get_sit(sit_name)	# creates sit
		if sit.line_of_def:
			self.error_line('cannot create situation "' + sit_name + '", already created in line ' + str(sit.line_of_def))
		sit.line_of_def = self.line_number
		# make current
		self.current_sit = sit
	def process_dir_line(self, direction, line, backdir=None):
		'allow a direction of movement and specify target, with two-way option'
		self.no_text()
		target_sit_name = self.get2of2(line)
		# FIXME - add possibility to _forbid_ an existing direction (by setting to zero)!
		self.add_sit_dir(direction, target_sit_name)
		if backdir:
			if self.cond_state != [0]:
				self.error_line('two-way directions cannot be used in "if" blocks')
			else:
				self.add_sit_backdir(target_sit_name, backdir)
	def process_dirs_line(self, dir1, dir2, line, two_way=False):
		'allow two directions of movement and specify targets, with two-way option'
		self.no_text()
		target_sit_name1, target_sit_name2 = self.get2and3of3(line)
		# FIXME - add possibility to _forbid_ an existing direction (by setting to zero)!
		self.add_sit_dir(dir1, target_sit_name1)
		self.add_sit_dir(dir2, target_sit_name2)
		if two_way:
			if self.cond_state != [0]:
				self.error_line('two-way directions cannot be used in "if" blocks')
			else:
				self.add_sit_backdir(target_sit_name1, dir2)
				self.add_sit_backdir(target_sit_name2, dir1)
	def process_const_line(self, line):
		'symbolic constant definition'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		name, value = self.get2and3of3(line)
		self.new_symbol(name)
		# get actual value
		num = self.get_num(value)
		self.consts[name] = num
	def process_enum_line(self, line):
		'enumerate symbolic constants'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		parts = line[4:].split(',')	# remove 'enum' keyword
		val = 0
		for name in parts:
			name = name.split()[0]	# remove spaces
			self.new_symbol(name)
			self.consts[name] = val
			val += 1
	def process_var_line(self, line):
		'variable declaration'
		#self.no_text()		this can actually be given inside of text as it does not inject code into output!
		name, start_value = self.get2and3of3(line)
		# get actual number for start value
		num = self.get_num(start_value)
		self.new_var(name, num)
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
		hinz = self.get_expr(parts[0])
		kunz = self.get_expr(parts[1])
		self.current_sit.add_code('+if_' + cmp[1] + ' ' + var_offset_label(hinz) + ', ' + var_offset_label(kunz) + ', .c_after' + str(self.cond_state[-1]))
	def end_cond_block(self):
		self.current_sit.add_code('+goto .c_end')
		self.current_sit.add_label('.c_after' + str(self.cond_state[-1]))
# if/elif/else/endif:
	def process_if_line(self, line):
		self.no_text()
		self.current_sit.add_code('!zone {')
		self.cond_state.append(1)	# go deeper, then in 1st block of if/elif/else/endif
		self.process_condition(line[3:])	# without "if"
		self.current_sit.change_indent(1)
	def process_elif_line(self, line):
		self.no_text()
		if self.cond_state[-1] == 0:
			self.error_line('Used ELIF without IF')
		if self.cond_state[-1] == -1:
			self.error_line('Used ELIF after ELSE')
		self.end_cond_block()
		self.cond_state[-1] += 1	# in next block of if/elif/else/endif
		self.current_sit.change_indent(-1)
		self.process_condition(line[5:])	# without "elif"
		self.current_sit.change_indent(1)
	def process_else_line(self, line):
		self.no_text()
		if line != "else":
			self.error_line('Garbage after ELSE?!')
		if self.cond_state[-1] == 0:
			self.error_line('Used ELSE without IF')
		if self.cond_state[-1] == -1:
			self.error_line('Used ELSE after ELSE')
		self.end_cond_block()
		self.current_sit.change_indent(-1)
		self.current_sit.add_code(';else')
		self.current_sit.change_indent(1)
		self.cond_state[-1] = -1	# in ELSE block of if/elif/else/endif
	def process_endif_line(self, line):
		self.no_text()
		if self.cond_state[-1] == 0:
			self.error_line('Used ENDIF without IF')
		if self.cond_state[-1] != -1:
			self.current_sit.add_label('.c_after' + str(self.cond_state[-1]))
		self.current_sit.add_label('.c_end')
		self.cond_state.pop()	# leave nesting level
		self.current_sit.change_indent(-1)
		self.current_sit.add_code('}; end of zone')
# var changing:
	def process_let_line(self, line):
		'writing to variable'
		self.no_text()
		parts = line.split('=')
		if len(parts) != 2:
			self.error_line('Line type not recognised')
		target_var = self.get_var(parts[0])
		# FIXME - make sure target var is not read-only!
		source_name = self.get_expr(parts[1])
		self.current_sit.add_code('+let ' + var_offset_label(target_var) + ', ' + var_offset_label(source_name))
	def process_incdec_line(self, what, line):
		'increment/decrement variable'
		self.no_text()
		var_name = self.get_var(self.get2of2(line))
		# FIXME - make sure var is not read-only!
		self.current_sit.add_code('+' + what + ' ' + var_offset_label(var_name))
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
			elif key == 'sit':
				self.process_sit_line(line)
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
			elif key == 'if':
				self.process_if_line(line)
			elif key == 'elif':
				self.process_elif_line(line)
			elif key == 'else':
				self.process_else_line(line)
			elif key == 'endif':
				self.process_endif_line(line)
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
		#self.current_sit.code.append(str(indents) + line)

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

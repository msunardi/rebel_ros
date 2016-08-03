import random, math

DEBUG = False

chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
acts = ['foo', 'bar', 'baz', 'right_arm', 'left_arm', 'turn_head_left', 'up', 'down', 'left', 'right', 'wander', \
		'calm', 'closed', 'wide', 'ramble', 'smile', 'frown', 'point', 'Face',]
ops = ['+', '&', '*']
Symbol = str
Env = dict
Number = (int, float)

def union(action1, action2, p=0.5):
	if DEBUG:
		print "%s, %s, %s" % (action1, action2, p)
	if (not isinstance(action1, Symbol) or not isinstance(action2, Symbol)):
		raise SyntaxError("Invalid action types! action1: %s, action2: %s." % (type(action1), type(action2)))
	if random.random() >= p:
		return action2
	return action1

def concatenate(action1, action2):
	return "%s%s" % (action1, action2)

# BUG: repeat should evaluate input
# Example:
# (a + b)* should yield: a, b, ab, aaaa, abab, abba, aaab, ...
# instead it's currently evaluating (a+b) first, then repeats that 
# Update 2/4/15: FIXED!
# Update 5/3/15: argument is now float (probability)
def repeat(expression, r=0.5):
	if DEBUG:
		print "%s, %s" % (expression, r)
	# if not isinstance(r, int) or r < 0:
	# 	raise SyntaxError("What the hell, man? What. The. Hell.")
	# if r > 4 and r <= 10:
	# 	print "%s times? Are you sure? OK ..." % (r)
	# elif r > 10:
	# 	print "%s times? Ha ha, yeah no, 10 it is." % (r)
	# 	r = 10
	out = ''
	# for i in range(random.randint(0,r)):
	# 	out = '%s%s' % (out, eval(expression))	# evaluate expression each repetition
	if random.random() <= r:
		out = '%s%s%s' % (out, eval(expression), repeat(expression, r))
	
	return out

# Source: norvig.com/lispy.html
def standard_env():
	env = Env()
	env.update(vars(math))
	env.update({
		'+': union,
		'&': concatenate,
		'*': repeat,
		'number?': lambda x: isinstance(x, Number),
		})
	return env

global_env = standard_env()

def tokenizer(expression):
	if DEBUG:
		print "Tokenizer - expression: %s" % (expression)
	return expression.replace('(', ' ( ').replace(')', ' ) ').replace('+', ' + ').replace('&', ' & ').replace('*', ' * ').split()

def read_from_tokens(tokens):
	if len(tokens) == 0:
		raise SyntaxError('Unexpected EOF')
		
	token = tokens.pop(0)
	# here process things in parenthesis
	if '(' == token:
		L = []
		while tokens[0] != ')':
			L.append(read_from_tokens(tokens))
		tokens.pop(0) # pop ')' right bracket
		return L
	elif ')' == token:
		return SyntaxError('Unexpected )')
	else:
		return atom(token)
	
def atom(token):
	try:
		return int(token)
	except ValueError:
		try:
			return float(token)
		except ValueError:
			return Symbol(token)

def parse(expression):
	return read_from_tokens(tokenizer(expression))

def eval(x, env=global_env):
	if DEBUG:
		print "x: %s" % (x)
	if isinstance(x, Symbol):
		if x in chars or x in acts: # if x is a variable, return as-is
			return "%s " % x
		return env[x]	# otherwise, x is an operator
	elif isinstance(x, Number):
		return x
	# TODO : probabilistic operator format: [p op] or [op p]?
	
	else:
		proc = eval(x[1], env)
		y = [x[0]]
		y.extend(x[2:])
		if proc.__name__ == 'repeat':	# If repetition, don't evaluate arguments
			#print "repeat!"
			args = y
		else:
			args = [eval(arg, env) for arg in y]
		if DEBUG:
			print "proc: %s" % (proc)
			print "args: %s" % (args)
	return proc(*args)

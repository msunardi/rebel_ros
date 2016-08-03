import random

chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ops = ['+', '&', '*']
Symbol = str
Env = dict

def standard_env():
	env = Env()
	env.update({
		'+': union,
		'&': concatenate,
		'*': repeat,
		})
	return env

def union(action1, action2):
	if random.random() >= 0.5:
		return action2
	return action1

def concatenate(action1, action2):
	return "%s%s" % (action1, action2)

def repeat(action):
	out = ''
	for i in range(random.randint(0,4)):
		out = '%s%s' % (out, action)
	return out

# Source: norvig.com/lispy.html
def tokenizer(expression):
	return expression.split(' ')

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
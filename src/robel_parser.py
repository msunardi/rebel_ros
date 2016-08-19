import random, math

DEBUG = False

chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
acts = ['foo', 'bar', 'baz', 'right_arm', 'left_arm', 'turn_head_left', 'up', 'down', 'left', 'right', 'wander', \
		'calm', 'closed', 'wide', 'ramble', 'smile', 'frown', 'point', 'Face', 'initial_stand', 'pause', 'head_to_512', \
		'legs_to_512', 'arms_to_512', 'stand', 'bow', 'head_40_left', 'head_90_left', 'head_40_right', 'head_90_right', \
		'look_down', 'look_up', 'hug', 'raise_arms', 'right_arm_wave', 'right_arm_down', 'left_arm_wave', 'left_arm_down', \
		'right_handshake', 'left_handshake', 'sit', 'squat', 'kneeling', 'left_lunge', 'right_lunge', 'right_splits', \
		'left_splits', 'right_front_kick_40', 'right_front_kick_90', 'right_kick_down', 'left_front_kick_40', \
		'left_front_kick_90', 'left_kick_down', 'right_side_kick_40', 'right_side_kick_90', 'right_side_kick_down', \
		'left_side_kick_40', 'left_side_kick_90', 'left_side_kick_down', 'right_back_kick_40', 'right_back_kick_90', \
		'left_back_kick_40', 'left_back_kick_90', 'right_knee_up', 'left_knee_up', 'legs_down', 'right_leg_lunge_forward', \
		'left_leg_lunge_forward', 'running_start', 'running_start_2', 'running_right_forward_1', 'running_right_forward_2', \
		'running_right_forward_3', 'running_left_forward_1', 'running_left_forward_2', 'running_left_forward_3', \
		'hands_in_the_air_1', 'hands_in_the_air_2', 'gasp', 'police_freeze_1', 'police_freeze_2', 'police_freeze_3', \
		'police_freeze_4', 'police_freeze_5', 'police_freeze_6', 'police_freeze_7', 'muscle_flex_1', 'muscle_flex_2', \
		'muscle_flex_3', 'muscle_flex_4', 'muscle_flex_5', 'muscle_flex_6', 'muscle_flex_7', 'onguard_1', 'onguard_2', \
		'onguard_3', 'onguard_4', 'onguard_5', 'onguard_6', 'yes_1', 'yes_2', 'yes_3', 'wow_1', 'wow_2', 'wow_3', 'wow_4', \
		'wave_1', 'wave_2', 'wave_3', 'wave_4', 'wave_5', 'yawn_1', 'yawn_2', 'yawn_3', 'brah_1', 'brah_2', 'brah_3', \
		'brah_4', 'brah_5', 'brah_6', 'brah_7', 'why_1', 'why_2', 'why_3', 'why_4', 'why_5', 'why_6', 'why_7', \
		'lookdownup_1', 'lookdownup_2', 'lookdownup_3', 'lookdownup_4', 'lookdownup_5', 'lookdownup_6', 'lookdownup_7', \
		'search_1', 'search_2', 'search_3', 'search_4', 'search_5', 'search_6', 'search_7', 'wave2_1', 'wave2_2', 'wave2_3', \
		'wave2_4', 'wave2_5', 'wave2_6', 'wave2_7', 'clap_1', 'clap_2', 'clap_3', 'clap_4', 'clap_5', 'clap_6', 'clap_7', \
		'oops_1', 'oops_2', 'oops_3', 'oops_4', 'oops_5', 'oops_6', 'muscle_combo_1', 'muscle_combo_2', 'combo_1', 'greeting',]
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

def parsex(exp):
    print "Evaluating: %s" % (exp)
    tokens = parse(exp)
    word = eval(tokens)
    print "Displaying: %s>>" % (word)
    return word

def foobarbaz(poo, vocab, loo=[], expansion=[]): #func, vocab):
    word = parsex(poo)
    expansion += [word]
    print "Word: %s" % word
    for c in word.replace('\n','').replace('\r','').split( ):
        cmd = vocab[c]
        print "%s: %s" % (c, cmd)
        if c in vocab.keys() and type(cmd) == str:
            foobarbaz(cmd, vocab, loo)
            continue
        print cmd
        loo += [cmd]
    else:
        print "Foobar!"
        print loo
    	return loo, expansion
#         break
#     logging.debug('foobarbaz done!')
    return
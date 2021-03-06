import random, math
from numpy.random import choice as npchoice
DEBUG = False

#########################
# SYMBOLS (also called 'Alphabet') - the list of symbols that REBeL can recognize
# chars : alphabet letters
# acts : names of poses for HROS-1 robot. Can be extended to poses or other commands for other robots.
#########################

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
        'oops_1', 'oops_2', 'oops_3', 'oops_4', 'oops_5', 'oops_6', 'muscle_combo_1', 'muscle_combo_2', 'combo_1', 'greeting',\
        'wave1', 'wave2', 'onguard', 'why', 'jumping', 'leila_dances', 'police_freeze', 'muscle_flex', 'yes', 'wow', 'yawn',\
        'brah', 'clap', 'oops', 'search', 'up', 'down', 'left', 'right']
        # 'wave3_0', 'wave3_1', 'wave3_2', 'wave3_3', 'wave3_4', 'wave3_5', 'wave3_6', 'jump1_0', 'jump1_1', 'jump1_2', 'jump1_3', 'jump1_4', 'jump1_5', 'jump1_6', 'pickupbox_0', 'pickupbox_1', 'pickupbox_2', 'pickupbox_3', 'pickupbox_4', 'pickupbox_5', 'victorypose_0', 'victorypose_1', 'victorypose_2', 'victorypose_3', 'victorypose_4', 'victorypose_5', 'victorypose_6', 'victorypose_copy1_0', 'victorypose_copy1_1', 'victorypose_copy1_2', 'victorypose_copy1_3', 'victorypose_copy1_4', 'victorypose_copy1_5', 'victorypose_copy1_6', 'wait_0_0', 'wait_0_1', 'wait_0_2', 'wait_0_3', 'wait_0_4', 'wait_0_5', 'wait_0_6', 'wait_1_0', 'wait_1_1', 'wait_1_2', 'wait_1_3', 'wait_1_4', 'wait_1_5', 'wait_2_0', 'wait_2_1', 'wait_2_2', 'wait_2_3', 'wait_2_4', 'wait_2_5', 'wait_2_6', 'alas_0', 'alas_1', 'alas_2', 'alas_3', 'alas_4', 'alas_5', 'alas_6', 'alas_mirror_0', 'alas_mirror_1', 'alas_mirror_2', 'alas_mirror_3', 'alas_mirror_4', 'alas_mirror_5', 'alas_mirror_6', 'alas_2_0', 'alas_2_1', 'alas_2_2', 'alas_2_3', 'alas_2_4', 'alas_2_5', 'alas_2_6', 'nope_nope_0', 'nope_nope_1', 'nope_nope_2', 'nope_nope_3', 'nope_nope_4', 'nope_nope_5', 'nope_nope_6',\
        # 'wave3', 'jump1', 'pickupbox', 'victorypose', 'victorypose_copy', 'wait_0', 'wait_1', 'wait_2', 'alas', 'alas_mirror', 'alas2', 'nope', 'waiting']
ops = ['+', '&', '*']
extension = ['|', '~'] 	# concurrent/parallel
ops = ops + extension
Symbol = str
Env = dict
Number = (int, float)
List = (list, tuple)

###############
# Operator definitions
###############

# def union(action1, action2, p=0.5):
#     if DEBUG:
#         print "%s, %s, %s" % (action1, action2, p)
#     if (not isinstance(action1, Symbol) or not isinstance(action2, Symbol)):
#         raise SyntaxError("Invalid action types! action1: %s, action2: %s." % (type(action1), type(action2)))
#     if random.random() >= p:
#         return action2
#     return action1
#
# def concatenate(action1, action2, p=1.0):
#     if 0.0 < p < 1.0:
#         if random.random() < p:
#             return "%s" % action1
#     return "%s%s" % (action1, action2)

# def union(*args):
#     if DEBUG:
#         print "[UNION] args:", args
#     # args = [a.strip() if type(a) == str else a for a in args]

#     action1 = args[0]
#     action2 = args[1:]
#     p = 0.5
#     try:
#         if type(args[-1]) == float:
#             p = args[-1]
#             if len(args[:-1]) == 2:
#                 action2 = args[1]
#             else:
#                 action2 = args[1:-1]

#             # clean up args
#             for c in action2:
#                 c = c.replace('\n', '').replace('\r', '')

#     except ValueError as ve:
#         # else:
#         #   action2 = args[1:]
#         pass

#     check_instances = [isinstance(arg, Symbol) for arg in action2[:-1]]
#     if not all(check_instances):
#         raise SyntaxError("Invalid action types!  %s." % check_instances)

#     if DEBUG: print "[UNION] p: %s" % p

#     if 0.0 < p < 1.0 and random.random() >= p:
#         if DEBUG:
#             print "[UNION] action2: %s" % [action2]

#         if type(action2) == tuple and len(action2) >= 2:
#             a2 = list(action2) + [p]
#             return union(*a2)
#         else:
#             return action2[0]
#     return action1

# UNION Operation
def union2(*args):
    """
    Randomly choose one symbol. Symbol: '+'.

    Parameters:
    *args (list): a list of symbols. If last argument is a float, it is used as probability.

    Example:
    >>> parsex('(+ a b)')
    a
    >>> parsex('(+ a b)')
    b
    """
    if DEBUG:
        print "[UNION] args:", args
    # args = [a.strip() if type(a) == str else a for a in args]
    actions = args
    p = None

    try:
        # Probability is given as list
        if isinstance(args[-1], List): # If last argument is a list of float, those are probabilities for choosing symbols.
            p = args[-1]
            actions = args[:-1]
            if len(p) != len(actions):
                raise Exception('List of probabilities must have the same size as the number of arguments.')

        elif isinstance(args[-1], Number):
            px = args[-1]   # If the last argument is one number, it is the probability for the first symbol; the remainder has probability 1-px.
            actions = args[:-1]
            py = 1.0 - px
            pz = py / (len(actions) - 1)  # The probability of the remainder of arguments is equally distributed
            p = [px] + [pz]*(len(actions) - 1)

    except TypeError as te:
        if type(args[-1]) == float: # If last argument is a float, it is used as probability.
            p = args[-1]
            actions = args[:-1]
        else:
            p = 1.0/len(args)
        actions = [c.replace('\n', '').replace('\r', '') for c in actions]

    except ValueError as ve:
        pass

    if DEBUG:
        print "Actions: ", actions
        print "p: ", p
    return npchoice(actions, p=p)

# CONCATENATION
def concatenate(*args):
    """
    Arrange symbols in a sequence. If last argument is a number/float, it is probability of evaluating the next symbol in *args.

    Parameters:
    *args (list): list of symbols to put in sequence

    Example:
    >>> parsex('(& a b c)')
    a b c
    >>> parsex('(& x c d)')
    x c d
    >>> parsex('(& a b c 0.5)')
    a b c   # Second and third symbols are evaluated
    >>> parsex('(& a b c 0.5)')
    a       # Second and third symbols are not evaluated
    """
    if DEBUG:
        print "[CONCATENATE] args: %s" % list(args)
    p = 1.0
    actions = args

    try:
        if float(args[-1]) and type(args[-1]) == float:
            p = args[-1]
            actions = args[:-1]
    except ValueError as ve:
        pass

    if 0.0 < p < 1.0:
        if random.random() > p:
            return "%s" % actions[0]
        else:
            if len(actions[1:]) < 2:
                return " ".join(actions)
            else:
                concat_args = list(actions[1:]) + [p]
                return "{0}".format(" ".join([actions[0], concatenate(*concat_args)]))

    return " ".join([str(i) for i in actions])


# BUG: repeat should evaluate input
# Example:
# (a + b)* should yield: a, b, ab, aaaa, abab, abba, aaab, ...
# instead it's currently evaluating (a+b) first, then repeats that
# Update 2/4/15: FIXED!
# Update 5/3/15: argument is now float (probability)
# REPETITION/
def repeat(expression, p=0.5):
    """
    Repeat symbols or re-evaluate expressions.

    Parameters:
    expression (string): a single symbol (no parenthesis), expression (a string with parenthesis).
    r (float): probability of evaluating expression. Default: 0.5 if not specified.

    Example:
    >>> parsex('(* a)')  # p = 0.5 (repeat zero or more times)
    a a a
    >>> parsex('(* a 2.5)')  # p = 2.5 (will repeat at least 2 times)
    a a
    >>> parsex('(* a 2.5)')
    a a a a a
    """
    if DEBUG:
        print "%s, %s" % (expression, p)
    # if not isinstance(p, int) or p < 0:
    # 	raise SyntaxError("Invalid probability type")
    # if p > 4 and p <= 10:
    # 	print "Will repeat %s times" % (p)
    # elif p > 10:
    # 	print "%s is too many. Will repeat 10 times." % (p)
    # 	p = 10
    out = ''
    # for i in range(random.randint(0,r)):
    # 	out = '%s%s' % (out, eval(expression))	# evaluate expression each repetition
    if p - 1.0 >= 0.0:
        # out = '%s%s%s' % (out, eval(expression), repeat(expression, r-1.0))
        out = '%s' % (" ".join([out, eval(expression), repeat(expression, p - 1.0)]))
        return out

    if random.random() <= p:
        # out = '%s%s%s' % (out, eval(expression), repeat(expression, r))
        out = '%s' % (" ".join([out, eval(expression), repeat(expression, p)]))
    return out

############################
# EXPERIMENTAL/NOT YET IMPLEMENTED
############################

def concurrent(*args):
    """
    Execute two or more things at the same time/concurrently.
    """
    if DEBUG:
        print "[CONCURRENT] args: %s" % list(args)
    # return action1 + '|' + action2
    if len(args) <= 1:
        return args[0] + ';'
    return " | ".join([c.strip() for c in [eval(args[0])] + [concurrent(*args[1:])]])


def merge(*args):
    """
    Combine two or more things into one - if possible.
    """
    if DEBUG:
        print "[MERGE] args: %s" % list(args)
    if len(args) <= 1:
        return args[0] + ';'
    return "~".join([c.strip() for c in [eval(args[0])] + [merge(*args[1:])]])

def predicate(*args):
    """
    Execute things under certain conditions.
    """
    # If-then [-else]
    test = args[0]
    if len(args) > 3:
        raise Exception('PREDICATE: too many arguments')
    elif len(args) == 2:
        if test():
            return eval(args[1])

    elif len(args) == 3:
        if test():
            return eval(args[1])
        else:
            return eval(args[2])
    return None

#####################
# PARSING METHODS
#####################
# Source: norvig.com/lispy.html
def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        '+': union2,
        '&': concatenate,
        '*': repeat,
        '|': concurrent,
        '~': merge,
        'if': predicate,
        'number?': lambda x: isinstance(x, Number),
        'list?': lambda x: isinstance(x, List)
        })
    return env

global_env = standard_env()

def tokenizer(expression):
    if DEBUG:
        print "Tokenizer - expression: %s" % (expression)
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').replace('+', ' + ').replace('&', ' & ').replace('*', ' * ').\
    replace('[', ' [ ').replace(']',' ] ').split()
    if DEBUG:
        print "Tokens: ", tokens
    return tokens

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
        return SyntaxError('Unexpected \')\'')
    elif '[' == token:
        M = []
        while tokens[0] != ']':
            M.append(read_from_tokens(tokens))
        tokens.pop(0)
        return M
    elif ']' == token:
        return SyntaxError('Unexpected \']\'')
    else:
        return atom(token)

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return Symbol(token)
            except ValueError:
                return list(token)

def parse(expression):
    return read_from_tokens(tokenizer(expression))

def eval(x, env=global_env):
    if DEBUG:
        print "x: %s" % (x)
    if isinstance(x, Symbol):
        if DEBUG:
            print "Symbol: %s" % (x)
        if x in chars or x in acts: # if x is a variable, return as-is
            return "%s " % x
        if x not in env:
            print "%s is neither a known symbol or an operator." % x
            return x
        return env[x]	# otherwise, x is an operator
    elif isinstance(x, Number):
        if DEBUG:
            print "Number: %s" % x
        return x
    elif isinstance(x, List) and all([isinstance(c, float) for c in x]):
        if DEBUG:
            print "List: %s" % x
        return x
    else:
        if DEBUG:
            print "Else, is not a symbol or number: %s" % x

        if not x:
            return 0

        # infix
        # proc = eval(x[1], env)
        # y = [x[0]]
        # y.extend(x[2:])

        # prefix
        proc = eval(x[0], env)
        y = x[1:]
        args = y

        if proc.__name__ == 'repeat':	# If repetition, don't evaluate arguments
            #print "repeat!"
            args = y
        else:
            args = [eval(arg, env) for arg in y]
        # args = [eval(arg, env) for arg in y]
        if DEBUG:
            print "proc: %s" % (proc)
            print "args: %s" % (args)
    return proc(*args)


def parsex(exp):
    """
    Main parsing method. Call this to evaluate an expression.
    An expression is a string which starts with ( and ends with ).
    An expression with only one symbol does not use parentheses.
    An expression is written in this format: '(<operator symbol> <symbol1> <symbol2> ... <symbolN> <optional: probability (float)>)'

    Returns:
    A string 
    """
    print "Evaluating: %s" % (exp)
    tokens = parse(exp)
    if DEBUG:
        print tokens
    word = eval(tokens)
    if DEBUG:
        print word
    print "Displaying >> %s" % (word)
    return word

def expand_sequence(sequence, vocab, loo=[], expansion=[]):
    """
    Parses an expression and expand the symbols into values if applicable.
    e.g. a symbol = a robot pose/joint angles
    """
    word = parsex(sequence)
    expansion += [word]
    print "Word: ", word
    for c in word.replace('\n','').replace('\r','').split():
        cmd = vocab[c]
        print "%s: %s" % (c, cmd)
        if c in vocab.keys() and type(cmd) == str:
            expand_sequence(cmd, vocab, loo)
            continue
        print cmd
        loo += [cmd]
    else:
        print "Foobar!"
        print loo
        return loo, expansion
#         break
#     logging.debug('foobarbaz done!')
#     return "Done"
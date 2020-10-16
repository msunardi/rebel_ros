# rebel_ros

ROS package for REBeL

## REBeL (Robot Expressive Behavior Language)

Create robot behaviors (sequence of actions) using algebraic operators.

### Symbols

Each symbol represents a robot behavior, e.g. a pose (joint angles), an action (e.g. blink LED). For example: a symbol for a wait pose is the string `'wait'`, the symbol for blinking LED can be the string `'blink'`. For example:

- `'wait' = [0.0, 0.0, 0.0, 0.0]` - the robot has 4 DOF and the joints are on position `0.0` for the `wait` pose.
- `'blink'` - when the robot receives the string `blink`, the robot blinks its LED.

In REBeL, symbols are strings - they could be a single letter, a word, or a sequence of words connected with underscore. They cannot have spaces in them. Symbols are case-sensitive. For example:

- `'wait_4_seconds'` (valid)
- `'wait 4 seconds'` (invalid)
- `'A'` (valid)
- `'a'` (valid, but different from `'A'`)

Symbols can be arranged in a sequence to create a sequence of actions. These are also called 'behaviors'. For example:

- `'wait_4_seconds blink'` - the robot will hold the `wait` pose for four seconds then blink its LED.

### Behavior Expression

Patterns or *families* of sequences of behaviors can be defined using *behavior expressions*. The format for a behavior expression is:

```
'(<operator> <symbol_1> <symbol_2> ... <symbol_n> <optional: probability>)'

```

A behavior expression is a string which starts with an open bracket `(` and ends with a closing bracket `)`. The first symbol inside the brackets is the *operator* (see next section) followed by the symbols for the pattern seperated by spaces. Optionally, you can specify probability values for all REBeL operators as the very last argument. If not given, default values are used (explained below).

Examples of behavior expression:
- `'(& a b c)' --> 'a b c'
- `'(+ a b c)' --> 'a' OR 'b' OR 'c'

### Operators

#### Concatenation

**Operator symbol**: `&`

**Function**: Arrange symbols in a sequence. For example:

- `'(& a b c)' --> 'a b c'

Concatenation can have probability value as argument. If the probability is a single value: applied to the second and subsequent symbols. For example: `(& a b c 0.5)'` the outcome can be one of: `'a', 'a b'`, or `'a b c'`. This is because after `'a'` there is 0.5 probability of continuing with the next symbol: `'b'`. If this fails, then the processing stops. If `'b'` had been chosen, then the same evaluation applies to `'c'`, and so on.

If you want to specify probability for each symbol, then provide a list of float values. For example: `'(& a b c [0.5, 0.2, 0.7])'`. The possible outcomes of this expression are:
- `''` or empty, if `'a'` is not evaluated due to the 0.5 probability.
- `'a'` will occur most of the time because the probability of evaluating `'b'` is very low at 0.2.
- `'a b'` and `'a b c'` - you get the idea.

#### Union

**Operator symbol**: `+`

**Function**: Choose one of the symbols. For example:

- `'(+ x y z)' --> 'x'` OR `'y'` OR `'z'`.

By default, union is a probabilistic operation. If no probability is specified, all arguments have the same probability. For example:

```
>>> parsex('(+ x y z)')
x
>>> parsex('(+ x y z)')
x
>>> parsex('(+ x y z)')
z
>>> parsex('(+ x y z)')
y
>>> parsex('(+ x y z)')
z
...
```

Probability can be specified in two ways: a single value, or a list of values.

If probability is a single value, the value is applied to the first symbol, and the remainder is divided equally to the remaining symbols. For example: `(+ x y z 0.4)` - P(x) = 0.4, P(y) = 0.3, P(z) = 0.3.

If the probability value is a list (the number of values must be equal to the number of symbols in the expression), then each value is the probability for each symbol in the same order. The values must sum to 1. Otherwise, REBeL will throw an error. For example: `(+ x y z [0.2, 0.2, 0.6])`.

#### Repetition

**Operator symbol**: `*`

**Function**: Evaluate an expression zero or more times. For example:
- `'(* a)'`

Repetition operation only need one argument. The argument can be a single symbol or an expression.

By default, union is a probabilistic operation. If no probability is specified, the default probability is 0.5. Because of this, repetition can produce *empty strings* which means 'do nothing'.

In repetition operation, you can give a probability value greater than 1, which instructs REBeL to evaluate that expression *at least* X times. For example:

- `'(* a 2.5)'` -- repeat at least twice
- `'(* a 1.0)'` -- repeat exactly once
- `'(* a 4.2)'` -- repeat at least four times, and so on.
- `'(* a 0.99999999)'` -- may cause infinite loops

### Nested Behavior Expression

Arguments for an operation can be another behavior expression. The nested behavior expression must follow the same format as described. If the expression-argument is selected, then REBeL will recursively evaluate the expression until each argument can no longer be expanded. For example:

- Concatenation: `'(& a (& x y) c d)'` Outcome: `'a x y c d'`
- Union: `'(+ (& a b) (& z x))'` Outcomes: `'a b'` OR `'z x'`
- Repetition of concatenation: `'(* (& a b))'` Outcomes: `''`(empty string) OR `'a b'` OR `'a b a b'` OR `'a b a b a b'` and so on.
- Repetition of union: `'(* (+ x y))'` Outcomes: `''`(empty string) OR `'x'` OR `'y'` OR `'x y'` OR `'x x'` OR `'x y x'` OR `'x x y'` and so on.

## Quick Start

Run the test program to try out different expressions and see their outcomes. (Tested on Python 3.6.8)

```
python test.py
```

The files you need for the test program to run are:
- `robel_parser.py` - The main program containing the parser, symbol definitions, and operator definitions. If you want to reuse REBeL in your own code, this is the one you must have.
- `makana_jimmy_program.py` - A Python script originally created by Makana Burch for use with HROS-1 robot. It has been modified for use with REBeL.
- `test.py` - The test script.

The rest of the files in this repository is for use with ROS.

## To Use with ROS

To use REBeL with ROS, run the server node:
```
rosrun rebel_ros rebel_server.py
```

To evaluate an expression, call the service either from command line or a ROS node. From command line:
```
$ rosservice call '(& a b c)'
```

To call from a node, see the `rebel_client.py` example.

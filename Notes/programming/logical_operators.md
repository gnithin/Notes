# Logical operators

This is super opinionated, with a dressing of logic to reinforce it :)

Suppose you have a function thats accepts 2 parameters - 

```
def super_critical_method(a, b):
	...
```
The very first step that needs to be done on a function like this is to validate the args `a` and `b`.

Assumption: The values can be null, None, nil or whatever the language supports. Let us assume that the `super_critical_method` still works properly, when any/all of the arguments are null. This assumption is necessary, since languages like `Swift` (and Python too) has the concept of optional and non-optional variables. Non-optional variables cannot be nil (the program won't compile), while optional can. So in Swift-speak, both these function arguments are optional, and the function needs to be handle them.

Before going further, let me establish what I think are the important characteristics of a good solution - 
- Clutter
	- Do you have to put a lot of mental effort in tracing through all the different paths? If so, that is what I'm referring to as clutter.
	- Why is clutter different from readability?
		- The same is the difference between a beautiful handwriting and a legible handwriting.
		- Beautiful handwriting looks neat on the outset. But when it comes down to reading it, you'll have to remember the minutiae of 'y' and an 'f'. That's significant mental load to consider all 13 pairs of the language.
	- Another side-effect of clutter is, if you have so much mental state to read it, if you have the misfortune to modify it, you might be likely to miss out important edge-cases. The code with low clutter (less moving parts as it were), will be much more easier to modify and maintain
- Understandability
	- This is a subjective metric, but is essential for ease of code-reading. Are you going to immediately grasp what the code is doing, if you look at it after a couple of years (without any comments, I might add)? Do you get the general idea of what a huge block of code can do, just by looking at a few top-level conditions?

Let us go through the myraid of ways that this can be done.



a = None
b = SomeObject()

# Tracing way (Not good)
if a != None:
	if b != None:
		# Both exist
	else:
		# Only b exists
else:
	if b != None:
		# Only b exists
	else:
		# Both don't exist

# More common way (I might be wrong)
if a != None and b != None:
	# Both exist
elif a != None or b != None:
	# Either One exists
	if a != None:
		# a exists
	else:
		# b exists
else:
	# Both don't exist

# Putting everything into one umbrella
if a == None or b == None:
	if a == None and b == None:
		# Both are None
	elif a == None:
		# a is None
	else:
		# b is None
else:
	# Both exist

# Using xor
if a != None xor b != None:
	# Either one exists
	if a != None:
		# a exists
	else:
		# b exists
elif a != None:
	# Both a and b exists
else:
	# Both a and b don't exist


Short circuit
exception in java

# For 3 vars




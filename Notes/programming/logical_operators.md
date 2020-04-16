# Logical operators

This post tries to think through the ways to write a frequently encountered task. This is super opinionated.

Suppose you have a function thats accepts 2 parameters - 

```
def super_critical_method(a, b):
	...
```
The very first step that needs to be done on a function like this is to validate the args `a` and `b`.
We can do this is in multiple ways. Even different languages/frameworks have different mechanisms to do this. Strongly typed languages, like TypeScript, try to perform this validation before this function is called, so that the function can directly use them. In weakly typed languages, like JavaScript, you would need to check the values inside the function. You can even write something like a middleware or a form of decorators, which perform the validation before the function is called. In any case, you would need to perform this check somewhere.

Assumption: The values can be null, None, nil or whatever the language supports. Let us assume that the `super_critical_method` still works properly, when any/all of the arguments are null. This assumption is necessary, since languages like `Swift` (and Python too) has the concept of optional and non-optional variables. Non-optional variables cannot be nil (the program won't compile), while optional can. So in Swift-speak, both these function arguments are optional, and the function needs to be handle them.

Let me put out what I think are the important characteristics of a good solution - 
### Clutter
	- Do you have to put a lot of mental effort in tracing through all the different paths? If so, that is what I'm referring to as clutter.
	- Why is clutter different from readability?
		- The same is the difference between a beautiful handwriting and a legible handwriting.
		- Beautiful handwriting looks neat on the outset. But when it comes down to understanding it, you'll have to remember the minutiae of variables named 'y' and 'f'. That's significant mental load to consider in featureful languages where many things seem like magic (cough ruby cough).
	- Another side-effect of clutter is, if you have so much mental state to read it, if you have the misfortune to modify it, you might be likely to miss out important edge-cases. The code with low clutter (less moving parts as it were), will be much more easier to modify and maintain

### Complexity
	- This is a subjective metric, but is essential for ease of code-reading. Are you going to immediately grasp what the code is doing, if you look at it after a couple of years (without any comments, I might add)? Do you get the general idea of what a huge block of code can do, just by looking at a few top-level conditions?
	- It is better to use functions that do one thing well. This will allow any kind of logic to fit in a much more fundamental way. Using a function that performs multiple things might make it look elegant, but as the logic grows, might lead to missed edge cases.

Let us go through the myraid of ways that this can be done.

a = None
b = SomeObject()

#### Tracing way (Not good)
```
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
```

#### Prioritizing both exist
```
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
```

#### Putting everything into one umbrella
```
if a == None or b == None:
	if a == None and b == None:
		# Both are None
	elif a == None:
		# a is None
	else:
		# b is None
else:
	# Both exist
```

#### Using xor (Short circuiting it)
```
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
```
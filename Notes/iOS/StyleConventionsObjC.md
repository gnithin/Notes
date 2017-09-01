### Style convention for Objective C

- Tab width - 4 (always)
- Function declaration style
	- Spaces in and around the methods and the formal parameters
- Declaring a lambda function style
- Never use _varName. Use self.varName instead
- All the singleton public instance getter names should be getSharedInstance
	- Not getInstance - The caller must know it's a singleton
	- Not sharedInstance - Function names must start with a verb
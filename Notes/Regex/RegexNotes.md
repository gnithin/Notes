## Regexes in python

Note: This is going to be about regexes in general and their usage in python. The text will be more regex heavy than python heavy.

What are regular expressions? 

Regular expressions are a concise way to describe a string or a group or strings. 
They are a shorthand, and as shorthands go, they have their own syntax.

A simple regex looks like this 
```
Regex to match english letters both lower and uppercase

Regex   -  [a-zA-Z]+
String  -  "Apple"
Matches -  ["Apple"]
```

A bit more involved, but comprehensible, regex looks like this
```
Regex to match hashtags in a string

Regex   -  #[a-zA-Z0-9\-_]+
String  -  "I need #help, please. #Thanks"
Matches -  ["#help", "#Thanks"]
```
[Source](http://stackoverflow.com/a/21651362/1518924)

While an insane regex looks like this 
```
Match strings surrounded by quotes that are not properties of an html tag

Regex   -  \"([^<>]*?)\"(?=(?:[^>]*?(?:<|$)))
String  -  "<p>This is a "wonderful text" <a href="site-to-nowhere.com" target="_blank">link</a>.</p>"
Matches -  ['"wonderful text"']
```
[Source](http://stackoverflow.com/a/22589854/1518924)

### Python and regex
Regexes come in many flavors. By that, I mean regex engines. The regex engine is the piece of code that basically evaluates a string against a regex. There are differences in the various regex flavors. The ones that we, as people who use them, need to be concerned about are regarding the feature set and the syntax that the engine has to offer.

Some of the regex flavors are - PCRE (Perl Compatible Regular Expressions), POSIX, .NET, JavaScript etc. Many individual programming languages have become a regex flavor because of the differences in their regex engines. Python's regex is it's own flavor :). There are also exceptions to that, like PHP whose regex engine is a wrapper around PCRE, which is written in C.

Regexes contain characters that have special meaning to them. Characters like `\` in `\d` shorthand character class are essential to the semantics of a regex. If we use them similar to the way we use strings(i.e enclosing them in double/single quotes) in python, they'll be treated as escape sequences. To use a backslash inside a string as a regex, we'll need to add two backslashes, `"\\d"`. A simpler solution is to use raw strings for regexes. In raw strings, the backslashes are not treated as a special character.

So a regex in python may be written as - 
```
regex = r'\d+'
```

In python, the `re` module exposes methods which are useful in processing strings using regexes.
Their [documentation](https://docs.python.org/3/library/re.html) is pretty much straight-forward about what they do.

Here is a list of functions that you might use and examples of how they work.

TODO: Add examples here!

## Important regex notations 

## Grouping 
- The indices of the capturing groups are depth first. Even in that, the order is Root - Children(Starting from the left-most). [Example here](https://regex101.com/r/X7fCOF/2)
<!--- If there is a combination of something like this - `(\w)+` the capturing group will only capture the last element and discard earlier ones. Make sure to use ((\w)+) if you need the whole thing. [Example here](https://regex101.com/r/1DFTOY/1)-->

## Backtracking

## Greediness and Laziness

## Lookaround

# Examples

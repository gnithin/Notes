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

Some of the regex flavors are - PCRE (Perl Compatible Regular Expressions), POSIX, .NET, JavaScript etc. Many individual programming languages have become a regex flavor of their own because of the differences in the implementation of their regex engines and what do and do not support. Python's regex is it's own flavor :). There are also exceptions to that, like PHP, whose regex engine is a wrapper around PCRE, which is written in C.

Regexes contain characters that have special meaning to them. Characters like `\` in `\d` shorthand character class(which matches a digit) are essential to the semantics of a regex. If we use them similar to the way we use strings (i.e enclosing them in double/single quotes) in python, they'll be treated as escape sequences. To use a backslash inside a string as a regex, we'll need to add two backslashes, `"\\d"`. A simpler solution is to use raw strings for regexes. In raw strings, the backslashes are not treated as a special character.

So a regex in python may be written as - 
```
regex = r'\d+'
```

In python, the `re` module exposes methods which are useful in processing strings using regexes.
Their [documentation](https://docs.python.org/3/library/re.html) is pretty much straight-forward and enlists the what the module can do.

Here is a list of functions that you might use and examples of how they work.

TODO: Add examples here!

Examples - 
```python
In [X]: import re
In [X]: ip_str = '''It is an ancient Mariner,
   ...: And he stoppeth one of three.
   ...: 'By thy long grey beard and glittering eye,
   ...: Now wherefore stopp'st thou me?
   ...:
   ...: The Bridegroom's doors are opened wide,
   ...: And I am next of kin;
   ...: The guests are met, the feast is set:
   ...: May'st hear the merry din.'''

In [X]: regex = re.compile(r'\b[a-zA-Z]+e\b')

In [X]: match_obj = regex.search(ip_str)

In [X]: match_obj.group()
Out[X]: 'he'

In [X]: regex.findall(ip_str)
Out[X]:
['he',
 'one',
 'three',
 'eye',
 'wherefore',
 'me',
 'The',
 'are',
 'wide',
 'The',
 'are',
 'the',
 'the']

# Using this is usually a lot more prudent for complex regexes or huge strings.
# It just returns an iterator
In [X]: match_iter = regex.finditer(ip_str)
In [X]: [val.group() for val in match_iter]
Out[X]:
['he',
 'one',
 'three',
 'eye',
 'wherefore',
 'me',
 'The',
 'are',
 'wide',
 'The',
 'are',
 'the',
 'the']

In [X]: re.split(r"[',.;]", ip_str)
Out[X]:
['It is an ancient Mariner',
 ' \nAnd he stoppeth one of three',
 ' \n',
 'By thy long grey beard and glittering eye',
 ' \nNow wherefore stopp',
 'st thou me? \n\nThe Bridegroom',
 's doors are opened wide',
 ' \nAnd I am next of kin',
 ' \nThe guests are met',
 ' the feast is set: \nMay',
 'st hear the merry din',
 '']

In [X]: for m in re.split(r"[',.;]",ip_str):
    ...:     val = m.strip()
    ...:     if val: print(val)
    ...:
It is an ancient Mariner
And he stoppeth one of three
By thy long grey beard and glittering eye
Now wherefore stopp
st thou me?

The Bridegroom
s doors are opened wide
And I am next of kin
The guests are met
the feast is set:
May
st hear the merry din

In [X]: print(re.sub(r'thy', "your", ip_str))
It is an ancient Mariner,
And he stoppeth one of three.
'By your long grey beard and glittering eye,
Now wherefore stopp'st thou me?

The Bridegroom's doors are opened wide,
And I am next of kin;
The guests are met, the feast is set:
May'st hear the merry din.

In [X]: def archaic_pronoun_conv(m_str):
    ...:     val = m_str.group().lower()
    ...:     if val == "thy":return "your"
    ...:     if val == "thou":return "you"
    ...:     if val == "may'st":return "may"
    ...:     return val
    ...:

In [X]: new_str = re.sub(r'thy|thou|May\'st', archaic_pronoun_conv, ip_str)

In [X]: print(new_str)
It is an ancient Mariner,
And he stoppeth one of three.
'By your long grey beard and glittering eye,
Now wherefore stopp'st you me?

The Bridegroom's doors are opened wide,
And I am next of kin;
The guests are met, the feast is set:
may hear the merry din.

```

## Important regex notations 

## Grouping 
- The indices of the capturing groups are depth first. Even in that, the order is Root - Children(Starting from the left-most). [Example here](https://regex101.com/r/X7fCOF/2)
<!--- If there is a combination of something like this - `(\w)+` the capturing group will only capture the last element and discard earlier ones. Make sure to use ((\w)+) if you need the whole thing. [Example here](https://regex101.com/r/1DFTOY/1)-->

## Backtracking

## Greediness and Laziness

## Lookaround

# Examples

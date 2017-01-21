## Regexes and Python

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

### Regexes in Python
Regexes come in many flavors. By that, I mean regex engines. The regex engine is the piece of code that basically evaluates a string against a regex. There are differences in the various regex flavors. The ones that we, as people who use them, need to be concerned about are regarding the feature set and the syntax that the engine has to offer.

Some of the regex flavors are - PCRE (Perl Compatible Regular Expressions), POSIX, .NET, JavaScript etc. Many individual programming languages have become a regex flavor of their own because of the differences in the implementation of their regex engines and what do and do not support. Python's regex is it's own flavor :). There are also exceptions to that, like PHP, whose regex engine is a wrapper around PCRE, which is written in C.

Regexes contain characters that have special meaning to them. Characters like `\` in `\d` shorthand character class(which matches a digit) are essential to the semantics of a regex. If we use them similar to the way we use strings (i.e enclosing them in double/single quotes) in python, they'll be treated as escape sequences. To use a backslash inside a string as a regex, we'll need to add two backslashes, `"\\d"`. A simpler solution is to use raw strings for regexes. In raw strings, the backslashes are not treated as a special character.

So a regex in python may be written as - 
```
regex = r'\d+'
```

In python, the `re` module exposes methods which are useful in processing strings using regexes.
Their [documentation](https://docs.python.org/3/library/re.html) is pretty much straight-forward and enlists the what the module can do.

Here is a list of functions that I commonly use. Refer to the [documentation](https://docs.python.org/3/library/re.html) here for more methods that `re` supports.

#### Search

`re.search(pattern, string, flags=0)`

It searches the input string for the first location of the a match against a regex. It stops after that. It returns a `match` object which basically stores information about the current match. You can fetch useful information like starting or ending index of the match, fetch part of the match corresponding to the capturing group by calling the appropriate `match` methods. You can read more about `match` [here](https://docs.python.org/3/library/re.html#match-objects)

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

# You can use compile if you think the regex is going to be used again.
# It's more efficient that way since everytime you need to match something against a regex, 
# a Regular Expression object will be created. 
# Note that even without using compile, re module caches the last used regex anyway, so creating them
# repeatedly should be fine I guess :) 
# Source: - http://stackoverflow.com/a/452143/1518924
In [X]: regex = re.compile(r'\b[a-zA-Z]+e\b')

In [X]: match_obj = regex.search(ip_str)

In [X]: match_obj.group()
Out[X]: 'he'
```

#### Findall

`re.findall(pattern, string, flags=0)`

This method basically finds all the non-overlapping matches in a string starting from left to right and returns a list of strings matches. When used with capturing groups, this returns a list of tuples.

```python
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
```

#### Finditer

`re.finditer(pattern, string, flags=0)`

If your regex is really complicated or if your string is really long or your requirments involving checking every string as they  matched one by one, then `finditer` is a good substitute for `findall`. It basically returns just an iterator which can be called repeatedly until the all the matches are exhausted. Using this is usually a lot more prudent when you need to save time or debug :)

```python
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
```

#### Split

`re.split(pattern, string, maxsplit=0, flags=0)`

This method is used to split the string based on a regex. It returns a list of strings just like how a string split would work.

```python
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
 ```

This is just a sanitized version of the previous string where empty values are removed

```python
# The ugly way :p 
# "\n".join([m.strip() for m in re.split(r"[',.;]",ip_str) if m.strip())])

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
```

Since you are using a regex to split, sometimes you will need the split string to also be produced in the output.
Using [capturing groups](TODO: Link to capturing groups), enables that. The splitting string is found between the matches. In case a splitting string is matched at the beginning of the input string, an empty string is the first element in the output. Moral of the story: Always sanitize your split outputs else you will have hell to pay :p

Here's a simple example that demonstrates that - 

```python
# Split the input strings by `_number_` and also fetch the numbers
In [X]: keycodes_str = "abcd_123_efgh_456_ijkl"

In [X]: re.split(r'_([0-9]+)_', keycodes_str)
Out[X]: ['abcd', '123', 'efgh', '456', 'ijkl']
```

#### Sub 

`re.sub(pattern, repl, string, count=0, flags=0)`


This method is used for finding a string matching a regex and then substituting it.

```python
In [X]: print(re.sub(r'thy', "your", ip_str))
It is an ancient Mariner,
And he stoppeth one of three.
'By your long grey beard and glittering eye,
Now wherefore stopp'st thou me?

The Bridegroom's doors are opened wide,
And I am next of kin;
The guests are met, the feast is set:
May'st hear the merry din.
```

The `sub` method also has this nice feature where instead of using the replacement string, you can pass a callback method that accepts a `match` object and will return a replacement string. This is useful when you want to perform some kind of logic.

```python
# This is basically replacing all the archaic pronouns into modern ones

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

All of the above methods have an optional argument called flags. The `re` module has some flags which basically modifies how a regex engines searches for a match against a regex. For example, using `re.I` or `re.IGNORECASE` will make the regex matching process case-insensitive. You can refer to a list of all the flags from their [documentation](https://docs.python.org/3/library/re.html#re.A). You can use multiple flags in python by bitwise or-ing them.

## Grouping 

- The indices of the capturing groups are depth first. Even in that, the order is Root - Children(Starting from the left-most). [Example here](https://regex101.com/r/X7fCOF/2)
<!--- If there is a combination of something like this - `(\w)+` the capturing group will only capture the last element and discard earlier ones. Make sure to use ((\w)+) if you need the whole thing. [Example here](https://regex101.com/r/1DFTOY/1)-->

## Backtracking

## Greediness and Laziness

## Lookaround

# Examples

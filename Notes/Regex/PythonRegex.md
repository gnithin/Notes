## Understanding the Python 3.5's re module

This is just an investigation of how python 3.5 basically parses regular expressions.

Basic tasks first, find out where the code actually lives.

Let's try - 
```zsh
➜  ~
$ which python3
/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
```

Ok, so the binary for python3 lives here. I need to find the source code. Let's dig deeper.
```zsh
# Let's go the directory which has python3 code
➜  ~
$ cd /Library/Frameworks/Python.framework/Versions/3.5/bin

# This directory seems to have all binaries. Let's search for something outside this.
➜  bin
$ cd ../
➜  3.5
$ cd lib/python3.5

# This directory seems to have everything, including re.py!
➜  python3.5
$ ls
LICENSE.txt         _weakrefset.py      cgitb.py            ctypes              formatter.py        imghdr.py           mailcap.py          pipes.py            random.py           socketserver.py     tarfile.py          types.py
__future__.py       abc.py              chunk.py            curses              fractions.py        imp.py              mimetypes.py        pkgutil.py          re.py               sqlite3             telnetlib.py        typing.py
__phello__.foo.py   aifc.py             cmd.py              datetime.py         ftplib.py           importlib           modulefinder.py     plat-darwin         reprlib.py          sre_compile.py      tempfile.py         unittest
__pycache__         antigravity.py      code.py             dbm                 functools.py        inspect.py          multiprocessing     platform.py         rlcompleter.py      sre_constants.py    test                urllib
```

Let's go through `re.py`. Here are it's basic highlights.
- The `re` module basically defines all acceptable constants and methods.
- The actual regex tasks seems to be done by `sre_compile` and `sre_parse`.
- The module is basically just a wrapper. It acts as an interface which maps the methods to those specified by `sre_compile`.
- The module is also responsible for caching the compiled regex.
- The caching is basically done using a dict. The compiled regex output is stored against a key.
- The key is basically (type, pattern, locale). 
- So something like `[a-z]` will produce the key like this - `(<class 'str'>, '[a-z]', 0)`
- The cache for the above entry looks kind of like this - 
  ```
  {(<class 'str'>, '[a-z]', 0): (re.compile('[a-z]'), None)}
  ```
- TODO: What is the significance of the locale here? Why is it separate from the regex? I thought it was supposed to be passed into it


The main crunching logic for python's regexes are basically in `sre_compile.py`, `sre_parse.py` and `sre_constants.py`.

### `sre_compile`
This module is basically responsible for creating getting a pattern and representing it in it's internal data structure.
- Every call to `compile` basically does this - 
    - Parse the input string using `sre_parse.parse` method. This takes in a regex pattern string and creates an internal structure. 
    - Here is an example - 
        - The output of one such structure for a simple pattern(`[a-z]`) is this - 
        ```
        Current expression -  [a-z]
        Parse output -
        [(IN, [(RANGE, (97, 122))])]
        ```
        - TODO: The part below is pure speculation. This will be confirmed, as soon as the internal mechanics of the regex engine is uncovered.
        - NOTE: From here on, anything like this will come with a `Speculation Alert!` disclaimer in bold.

        - __Speculation alert! ON__
        - It looks like it's creating a list of individual commands, (tokens would have been a more correct term I guess) that the regex engine needs to follow.
        - __Speculation alert! OFF__

        - Note: The output is not a list. It's a `sre_parse.SubPattern` type, that's been stringified.

        - For something a little bit more involved - `[a-z]\w*(?:\.\w{1,3})+`
        ```
        ****************************************
        Current expression -  [a-z]\w*(?:\.\w{1,3})+
        Parse output -
        [(IN, [(RANGE, (97, 122))]), (MAX_REPEAT, (0, MAXREPEAT, [(IN, [(CATEGORY, CATEGORY_WORD)])])), (MAX_REPEAT, (1, MAXREPEAT, [(SUBPATTERN, (None, [(LITERAL, 46), (MAX_REPEAT, (1, 3, [(IN, [(CATEGORY, CATEGORY_WORD)])]))]))]))]
        ****************************************
        ```
        - Formatting this a little bit, there are a couple of interesting things that come up, which has been elaborated on below in the comments.
        ```
        [
            # [a-z]
            (IN, [(RANGE, (97, 122))]),

            # \w* (MAX_REPEAT seems to be a token, while MAXREPEAT seems to be a constant denoting infinity. The naming convention sucks here <sidenote>Potential contribution candidate :p</sidenote>)
            (MAX_REPEAT, (0, MAXREPEAT, [(IN, [(CATEGORY, CATEGORY_WORD)])])),

            # Question: MAX_REPEAT seems to follow (min_iterations, max_iterations, list_of_tokens). 
            # Why does the third object need to be a list? Couldn't it be a normal pattern? 
            # Whenever I need to add quantifiers to a bunch of stuff, grouping constructs like `(?:)` or `()` are used,
            # Which is basically one whole new regex used as a subexpression as you will see below. 
            # The only thing that strikes me is that it's been kept to support the uniform notion of regexes as a list of tokens
            # everywhere. That kind of makes sense I guess. I would do that :p

            # (?:\.\w{1,3})+ 
            (MAX_REPEAT, 
                (
                    1, MAXREPEAT, [
                        (
                            SUBPATTERN, (
                                None, [
                                    # Matches the literal "."
                                    (LITERAL, 46), 

                                    # \w{1,3}
                                    (MAX_REPEAT, (1, 3, [(IN, [(CATEGORY, CATEGORY_WORD)])]))
                                ]
                            )
                        )
                    ]
                )
            )
        ]
        ```
        - __Speculation alert! ON__ 
        - So as an overview of how this piece fits, the regex engine receives this as the input regex, to match against a string.
        - The regex engine, tries to match element in the list sequentially, one by one.
        - I guess for tokens like SUBPATTERN, this same logic is recursively called again, for it's contents.
        - __Speculation alert! OFF__ 

### `sre_parse`
- NOTE: Try out a couple of python in-code debuggers. Maybe the one that ships with proper IDEs, like that one <Whatever it's name is>.
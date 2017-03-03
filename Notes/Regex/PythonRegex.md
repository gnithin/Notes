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
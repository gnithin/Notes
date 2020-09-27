# Character sets 
So this is a subject that I need to brush once every year since I seem to forget it, every single darn time I encounter any character-set problems (Almost makes me wonder, what if there was a leet-code style problem set which required us to understand unicode standard, as an interview. I would love that. But I dream).


## Basics 
Refer to this article - https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/

Unicode is a standard used for codifying the characters on the screen. All letters are mapped to a code-point, like U+0012, which is just a number. This represents a character.

For representing these code-points in memory, you need encodings. UTF-8 stores between 2 to 6 bytes. Not all ecodings can store all the code-points. But encodings like UTF 7, 8, 16, 32 can store all of them correctly.

## How python handles it 
- Article - https://www.b-list.org/weblog/2017/sep/05/how-python-does-unicode/

Unicode has this property to combine multiple code-points (decomposed form), and generate a new code-point (composed form).

- QUESTION - If UCS-2 is 2 bytes, how would it handle code-points that require > 2 bytes? Unicode contains more than 2^16 entries. It would either break it up into subsequent code-points or truncate stuff. What does it do?

The answer to the above question lies in surrogate pairs. Basically convert the given entries into 2 UTF-16 entries (or 2 bytes each, 4 bytes total). The unicode standard is limited to 21 bits overall, so anything of the 21 bit entries can be represented as a surrogate pair in UTF-16 (and as a result in UCS-2 as well). The surrogate pairs are called high and low surrogate pairs respectively.
- Another good resource for surrogate pairs - https://unicodebook.readthedocs.io/unicode_encodings.html#utf-16-surrogate-pairs

NOTE: UTF-16 uses 2 or 4 bytes (It's not fixed!). Although UCS-2 is always 2 bytes (Also, UTF-32 is always 4 bytes)

An important point here is to understand that composition and surrogate pairs are different things.
- A composition is combining 2 unicode code-points to create another code-point. The 2 code-points are valid unicode entries, with a grapheme attached to them.
- Surrogate pairs are UTF-16 encoding concept. They don't exist in unicode. They are a way to support those code-points that need more than 16 bytes to be represented. So UTF-16 eventually represents them in 2 2-byte pairs. This is a surrogate pair.

So this is the most important thing that I've read (also this page has a lot of awesome snippets, just that it's written in an extremely non-noob way, so I need to re-read everything) - 
Python interpreters from 2.x to 3.3 has 2 flavors. They are called narrow and wide builds. This choice was made when the python interpreter was compiled (read that again, it's not your code, but when the interpreter was compiled). We can figure it out quite simply by using sys call, as used [here](https://stackoverflow.com/questions/1446347/how-to-find-out-if-python-is-compiled-with-ucs-2-or-ucs-4)

Here's the PEP that talks about this - https://www.python.org/dev/peps/pep-0261/
This is surprisingly readable. It basically weighs the pros and cons of doing it both ways. Kind of similar to an RFC I guess.

In narrow build, unicode strings were stored in 2 bytes blocks, with surrogates being represented as 2 separate entries. In the wide build, 4 byte encoding was used, so a surrogate needn't exist at all in the first place! (Holy shit!)

- Basic Multilingual Plane - https://www.sttmedia.com/unicode-basiclingualplane
- All the chars within unicode code-points (0 - 2^16 - 1) come under this. These can be represented properly within 2 bytes exactly.
- There are other planes, which make up for the rest of the bits in 2^21 size limit of unicode code-points. In UTF-16 (UCS-2), they are represented using 2 2-byte pairs, or 4 bytes overall, called surrogate pairs.

## Must read 
- TODO: https://kunststube.net/encoding/






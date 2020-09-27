# Understanding unicode
So this is a subject that I need to brush once every year since I seem to forget it every single darn time I encounter any character-set problems (Almost makes me wonder, what if there was a leet-code style problem set which required us to understand unicode standard, as an interview. I would love that. But I dream).

Articles referred to - 
- https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
- https://www.b-list.org/weblog/2017/sep/05/how-python-does-unicode/
- https://kunststube.net/encoding/


## Basics 
Unicode first and foremost defines a table of characters to code points. Unicode is a standard used for codifying the characters on the screen. All characters arerepresented by a code-point, like U+0012, which is just a hex number. The visual representation of a code-point is called a grapheme. We can render the same code-point in different fonts. The font won't change what the code-point is.


For representing these code-points in memory, you need encodings. The code-points range from numbers 0-2^21. So an encoding with upto 4 bytes should be able to store everything (Although it'd be wasteful to do so) - 
- UTF-8 - between 1 to 4 bytes. This is backwards compatible with ascii.
- UTF-16 - Between 2 to 4 bytes.
- UTF-32 - Fixed length - 4 bytes. Yugge waste.
- Not all encodings can store all the code-points. But encodings like UTF 7, 8, 16, 32 can store all of them correctly.

### Basic Multilingual Plane 
- Refer - https://www.sttmedia.com/unicode-basiclingualplane

Initially it was thought that 2 bytes or 2^16 possibilities was enough to represent all the characters. That was wrong. So later on, more code-points were introduced. So these code-points are named differently based off of which numerical region they lie in, called the multi-lingual plane (What a fancy name!).

The first and the most commonly used numerical regions is between 0 - 2^16 called the basic multi-lingual plane (BMP). UTF-16 and UCS-2 both support these fully . 

### Surrogate pairs
For code-points that are outside the BMP, UTF-16 converts them into 2 UTF-16 characters (4 bytes total) called surrogate pairs. Note that the individual code-points in the surrogate pairs don't map to anything (this is intentional apparently).


The unicode standard is limited to 21 bits overall, so anything of the 21 bit entries can be represented as a surrogate pair in UTF-16 (and as a result in UCS-2 as well). The surrogate pairs are called high and low surrogate pairs respectively.

Unicode has this property to combine multiple code-points (decomposed form), and generate a new code-point (composed form). This is different from surrogate pairs, which is a encoding (UTF-16) specific construct, while composition is a unicode standard specific construct.

QUESTION - If UCS-2 is 2 bytes, how would it handle code-points that require > 2 bytes? Unicode contains more than 2^16 entries. It would either break it up into subsequent code-points or truncate stuff. What does it do? 

The answer to that is to use surrogate pairs, since UTF-16 will represent them with 2 2-bytes.

Another good resource for understanding surrogate pairs - https://unicodebook.readthedocs.io/unicode_encodings.html#utf-16-surrogate-pairs

An important point here is to understand that composition and surrogate pairs are different things.
- A composition is combining 2 unicode code-points to create another code-point. The 2 code-points are valid unicode entries, with a grapheme attached to them.
- Surrogate pairs are UTF-16 encoding concept. They don't exist in unicode. They are a way to support those code-points that need more than 16 bytes to be represented. So UTF-16 eventually represents them in 2 2-byte pairs. This is a surrogate pair.

## How python handles unicode

- Article - https://www.b-list.org/weblog/2017/sep/05/how-python-does-unicode/

The unicode string stores a sequence of code-points.

So this is the most important thing that I've read (also this page has a lot of awesome snippets, just that it's written in an extremely non-noob way, so I need to re-read everything) - 


Python interpreters from 2.x to 3.3 has 2 flavors. They are called narrow and wide builds. This choice was made when the python interpreter was compiled (read that again, it's not your code, but when the interpreter was compiled). We can figure it out quite simply by using sys call, as used [here](https://stackoverflow.com/questions/1446347/how-to-find-out-if-python-is-compiled-with-ucs-2-or-ucs-4)

Here's the PEP that talks about this - https://www.python.org/dev/peps/pep-0261/
This is surprisingly readable. It basically weighs the pros and cons of doing it both ways. Kind of similar to an RFC I guess.

In narrow build, unicode strings were stored in 2 bytes blocks, with surrogates being represented as 2 separate entries. In the wide build, 4 byte encoding was used, so a surrogate needn't exist at all in the first place! That's the reason why there's a difference when using the `len` function between both of them.

## More detailed notes
- Article: https://kunststube.net/encoding/
NOTE: This is a must read. More than the Spolsky article!

Unicode is a table that maps characters to code-points. A code-point is a number (represented in hex), preceded by a "U+" which indicates it's a unicode code-point.

Assuming that all the encodings that are supported by a machine/software uses unicode to map from code-point to character, we still need to know the encoding of the string before the machine can parse it.

A set of bytes can be interpreted differently by different encodings, and may lead to printing garbled text. More often than not, garbled text is a result of the wrong encoding rather than the data being corrupted. 

Data can be corrupted, if we assume the wrong encoding, and re-save that string in that encoding. So it remains garbled forever. This is reversible if we would know the exact chain of events that happen, but that is hard.















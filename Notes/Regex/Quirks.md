## Awesome regex quirks 
Awesome is purely subjective ofcourse :p
 
- Using \c* matches j - https://regex101.com/r/cWOy3i/1
  http://www.regular-expressions.info/nonprint.html
  Using characters other than letters after \c is not recommended because the behavior is inconsistent between applications. Some allow any character after\cwhile other allow ASCII characters. The application may take the last 5 bits that character index in the code page or its Unicode code point to form an ASCII control character. Or the application may just flip bit 0x40. Either way \c@ through \c_ would match control characters 0x00 through 0x1F. But \c* might match a line feed or the letter j. The asterisk is character 0x2A in the ASCII table, so the lower 5 bits are 0x0A while flipping bit 0x40 gives 0x6A. Metacharacters indeed lose their meaning immediately after\cin applications that support \cA through \cZ for matching control characters. The original JGsoft flavor, .NET, and XRegExp are more sensible. They treat anything other than a letter after\cas an error.

- In Perl, the mode where the dot also matches line breaks is called "single-line mode". This is a bit unfortunate, because it is easy to mix up this term with "multi-line mode". Multi-line mode only affects anchors, and single-line mode only affects the dot. You can activate single-line mode by adding an s after the regex code, like this: m/^regex$/s;.

- You can overcome the fixed length matching of lookbehinds, by using multiple lookbehinds. Here's an [example](http://stackoverflow.com/a/22595535/1518924) , something like this - `r'(?<!Mr)(?<!Mrs)(?<!Ms)(?<!Esq)(?<!e.g)(?<!i.e)[.?]\s+'
`

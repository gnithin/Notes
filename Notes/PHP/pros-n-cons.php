What I don't like about php -
- Different extensions for mysql (There has to be only one proper way to do stuff and migrating between them is HARD)
- Using references introduces a bucket-load of hard to debug bugs - (Eg: Always set the ref as null after using it, especially when used inside a foreach )
- Library bugs ( Eg: mb_substr has length param as upper bound on number of CHARs to use (Even if encoding is provided). It's actually the number of bytes, the community doesn't accept that as an error, but it was supposedly intended )
- `utf8_encode` is badly named. It's supposed to convert from ISO-8859-1 to utf-8. It ain't a magic wand.
- Inconsistency in function details. For example - 
  ```
  array_map	 ( callable $callback, array $array1...)
  array_filter ( array $array, callable $callback...)
  ```
  `array_filter` could have the args order similar to `array_map`.

- Sometimes, really Bad error messages ( for mutiple includes of same file )- 
  ```
  ( ! ) Fatal error: Cannot redeclare sendMail() (previously declared in /exposure-server/src/frontend/app/include/sendmail.php:18) in /exposure-server/src/frontend/app/include/sendmail.php on line 18
   Call Stack
   #	Time	Memory	Function	Location
   1	0.0011	230024	{main}( )	../setup.php:0
   2	0.0200	474344	require( '/exposure-server/src/frontend/app/test.php' )	../setup.php:131
  ```
- Can't have str numeric keys for dicts
- `foreach` variable naming is counter intuitive : `foreach($arr as $a_content)` as opposed to - `for $a_content in $arr`  used in python, bash.
  (Not really a disadvantage, but more of a complaint. Inversely, PHP guys might complain about python :P)

Things I like about php - 
- Easy to learn - C like syntax
- Simple to setup and get it running (Rewrite rules not mandatory for a server)
- Stackoverflow php tag is kickass and vibrant and opinionated.
- Awesome array_* functions - Eg: `array_count_values()`. If you ever need to do anything on an array, there's probably a function for it.
- Really simple module imports (based on current file execution or the import files path or absolute whatever is necessary)
- Really simple file handling functions (C-like)
- Handling Cookies and sessions is really simple.
( Unlike stuff like express js where handling cookies need to look around for methods in request and response objects )

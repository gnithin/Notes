I've been trying to understand how git works internally. I've often heard of git-objects, and never fully understood them. This is an attempt to understand them properly.

I am going to be writing Notes trying to understand this [lesson](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain).

- Plumbing and Porcelain - [This](https://stackoverflow.com/a/6976506/1518924) nice answer explains the context. Note that the porcelain in stuff like `git status --porcelain` is usually used for getting computer parsable output, while the porcelain that they seem to refer here is about making the human understandable abstraction layer for using Git. I think these two contradict, or maybe they use this term to mean "polished" or "clean"

## Git objects
### Types of objects
- There seems to be different types of objects in git. Using `git cat-file -t`, I can get them. So the ones I found are `blob`, `tree`, `commit`.
- Every git commit is a git object which contains a reference to a tree object, author, committer (don't know the difference here) and the commit message.
```
➜  trial git:(master)
$ git --no-pager log --pretty=oneline
cf63d747a1ee4eb8507448971a849cebfc7264ff TEMP
➜  trial git:(master)
$ git cat-file -t cf63d747a1ee4eb8507448971a849cebfc7264ff
commit
➜  trial git:(master)
$ git cat-file -p cf63d747a1ee4eb8507448971a849cebfc7264ff
tree 90017a36095404dd975a165e62518c70ec1565c5
author Nithin <nithin.linkin@gmail.com> 1538864107 +0530
committer Nithin <nithin.linkin@gmail.com> 1538864107 +0530

First Commit
```
- Tree object contains the blob and the file name. Trees essentially map file-names to blobs. They can also contain other trees. They correspond to a directory in file-system lingo.
```
➜  trial git:(master)
$ git cat-file -p 90017a36095404dd975a165e62518c70ec1565c5
100644 blob b14df6442ea5a1b382985a6549b85d435376c351    init.txt
```
- Blob contains the actual file
```
➜  trial git:(master)
$ git cat-file -p b14df6442ea5a1b382985a6549b85d435376c351
Hi
```

### How is content actually stored in git-blob object?
- Using `git cat-file -p <SHA-1>`, the contents of a blob is visible.
- Opening up an actual blob file, the data is purely in hex. Hex-dumping it does not seem to give anything useful. 
```
➜  trial git:(master)
$ git cat-file -p b14df6442ea5a1b382985a6549b85d435376c351
Hi
➜  trial git:(master)
$ hexdump -C .git/objects/b1/4df6442ea5a1b382985a6549b85d435376c351
00000000  78 01 4b ca c9 4f 52 30  66 f0 c8 e4 02 00 11 43  |x.K..OR0f......C|
00000010  02 ae                                             |..|
00000012
```
- A git object is stored like this - 
    - Create header 
        - "<TYPE> <CONTENT-LENGTH>\0"
        - For example - "blob 12\0"
    - git-object contents = Header + Contents
    - The SHA-1 of above is the hash, and the name of the object
    - The contents are zlib'ed
    - The first two chars in the SHA represent the directory and the rest the file-name. I am not sure why this is required.
        - Apparently it is useful in systems which get slower if number of files in a folder is huge, and also for something called packing heuristics. [Source](https://stackoverflow.com/questions/30662521/advantages-of-categorizing-objects-into-folders-named-as-the-first-2-characters)
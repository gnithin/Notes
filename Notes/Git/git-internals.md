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
    - NOTE: The commit object also contains the hash of the parent commit object as well. I guess, in case of a merge, it contains 2 parent commits.
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
        - `<TYPE> <CONTENT-LENGTH>\0`
        - For example - `"blob 12\0"`
    - git-object contents = Header + Contents
    - The SHA-1 of above is the hash, and the name of the object
    - The contents are zlib'ed
    - The first two chars in the SHA represent the directory and the rest the file-name. I am not sure why this is required.
        - Apparently it is useful in systems which get slower if number of files in a folder is huge, and also for something called packing heuristics. [Source](https://stackoverflow.com/questions/30662521/advantages-of-categorizing-objects-into-folders-named-as-the-first-2-characters)

## Git Refs
- References are files with git object hashes. 
- These hashes are generally commit hashes
- Since all the commits have a parent information, if we have a commit, we can travel down upto the starting commit
- So basically a branch is just a ref with a commit-hash
    - This is so awesome
    - I guess at the time of merging git tries to find the common point of intersection. That's a pretty cool problem to solve efficiently
- Three types of references - 
    - HEAD
    - Tag
    - Remote
- A head is symbolic reference. Symbolic reference is a file that stores another file's path, which stores the actual object-has
    - Basically pointer to a pointer
    - Head tells you what branch you are on
    - The refs for that branch will tell you which commit you are on
- A tag is like a branch that can't be updated.
    - Lightweight tags -
        - Just create them without any metadata
        - It's just a ref with a commit-hash
    - Annotated tags - 
        - It's a tag with meta-data of who tagged it
        - It stores an object hash, which is basically something similar to a commit-hash, but which points to a commit-hash (unlike a commit-hash which stores a tree-hash), and other meta-data
        - This could also mean that you can manually store anything other than a commit-hash in a annotated tag
        - The below is just me having some fun - 
            ```
            ➜  trial git:(master)
            $ echo "Kamehameha" | git hash-object --stdin
            5fc1a44cae2ce8775b9095f89844b26fc0bf67d4
            ➜  trial git:(master)
            $ echo "Kamehameha" | git hash-object -w --stdin
            5fc1a44cae2ce8775b9095f89844b26fc0bf67d4
            ➜  trial git:(master)
            $ git tag -a who-am-i 5fc1a44cae2ce8775b9095f89844b26fc0bf67d4 -m "Identity"
            ➜  trial git:(master)
            $ git tag --list
            who-am-i
            ➜  trial git:(master)
            $ git cat-file -p 5fc1a44cae2ce8775b9095f89844b26fc0bf67d4
            Kamehameha
            ➜  trial git:(master)
            $ git cat-file blob who-am-i
            Kamehameha
            ➜  trial git:(master)
            $ gti checkout who-am-i
            fatal: reference is not a tree: who-am-i
            ```
### Packing
- Observation - When a modification in a file is performed, a new blob consisting of the entire file seems to be constructed. This seems highly inefficient. I thought they were storing the line-number and the modified line so that it'll be compact or something. The advantage of this method is that you can very quickly jump between commits/branches, which would mean that you are only loading the data from the tree directly. The diff method would entail traversing the commit history. I guess I was wrong, this method seems much better, although it might take up more space in case of larger files
- The above observation seems unoriginal since the people who made git took care of that. The compress files and store deltas in something called as packing. It's run whenever pushing to remote or manually when running `git gc`.
- I don't understand the specifics of this. Need to work harder at that.
- Running `git gc` manually, kinda removed all of the git objects into a pack directory

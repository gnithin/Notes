# Private pods in Cocoapods

- Paraphrasing official [`docs`](https://guides.cocoapods.org/making/private-cocoapods.html)
- This is basically useful for creating and distributing apps inside an organisation
- This is especially applicable to private repositories

###  Creating a private pod spec source

- Suppose you have a `DemoLib`, with a private repo in github
- Create a private repo inside your organisation, in github, with the name `my-specs` (The full repo path will be denoted by `<my-specs.git>`)

```
# Add the private repo to your local Cocoapods specs list
$ pod repo add <my-specs> <my-specs.git>

# Check presence (Confirmation of previous step)
$ ls ~/.cocoapods/repos
master         my-specs

# Push your podspec to this repo
$ pod repo push --verbose my-specs ./demo-lib.podspec.json --allow-warnings
```

### Using a private pod
In final app's `Podfile`, add these 2 lines - 
```
# At the top of the file (After use_frameworks!, if present)
source '<my-specs.git>'
source 'https://github.com/CocoaPods/Specs.git'
...
pod 'DemoLib'
...
```

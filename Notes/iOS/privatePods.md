# Private pods in Cocoapods

- Paraphrasing official [`docs`](https://guides.cocoapods.org/making/private-cocoapods.html)
- This is basically useful for creating and distributing apps inside an organisation
- This is especially applicable to private repositories
- All the examples I've added are tested, so it should be working properly. Also, the Cocoapods version I use is - `1.2.0`

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
```ruby
# At the top of the file (After use_frameworks!, if present)
source '<my-specs.git>'
source 'https://github.com/CocoaPods/Specs.git'
...
pod 'DemoLib'
...
```

### Adding a private pod as a dependency in a podspec
You can add the private pod just like adding normal dependency in the podspec file.

For instance, if you have another library - `SecondLib`, which needs to use `DemoLib`, then add it to the dependency like this - 

```ruby
# Podspec file (SecondLib.podspec)
Pod::Spec.new do |s|
    s.dependency 'DemoLib', '1.0.0'
end
```

Then in Podfile of the app that uses `SecondLib`, the sources needs to be specified (Just like how you'd specify the sources for incorporating a private pod in your app)

```ruby
# Podfile of the app that uses `SecondLib`
source '<my-specs.git>'
source 'https://github.com/CocoaPods/Specs.git'
...

pod 'SecondLib'

...
```

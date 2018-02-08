# iOS Q&A

### What does apple do when it signs an ipa for distribution?

### Why can't I decrypt an ipa without jail-breaking?

### How does injection fit into this picture?

### What is an ipsw?

### What does it mean by saying "Apple stopped signing ipsw"? How does it impact anything?

### Are ipas hardware and ios version specific? Can I run the same ipa on different ios hardwares and devices?

### What is the meaning of "encryption/decryption at the hardware level"?

### How do encrypted ipas work on iphones?
Mach-O files can be encrypted. That is the case with the executable files of App Store apps. This encryption can be decrypted (on a hardware level) only on the device for which this build of the app is intended.[5]

### How can we decrypt an ipa?
The only way to decrypt encrypted binary data is on a jailbroken device with a few special tools installed.[5]

### What does jail-breaking mean exactly, technically?
Jailbreaking basically disables all the code signing and sandboxing security infrastructure in the phone.[2]
Apple’s iOS software is prone to jailbreaking, meaning Apple’s security features are surpassed to gain root privileges or system administration capabilities. One can run unsigned code on devices that are jailbroken.[5]

### Difference signing vs encryption
They both are different. A signed app, is just the app and other code that contains the checksum and the signing identifier.
Encryption is the process of encrypting the whole binary, so that in order to actually run it, it is first, required to decrypt the app.
iOS apps from the store are signed and then encrypted. The decryption happens at the hardware level only. 

### Difference between armv7 & arm64?
They are CPU architectures for iOS devices.[5] There are others as well - armv6, armv7, armv7s, arm64

### What is an ipa?
This .ipa is a compressed directory containing the app bundle and additional resources needed for App Store services, such as .dSYM files for crash reporting and asset packs for On Demand Resources.[1]

### How does provisioning profile fit into ipas?
A privisioning profile is a file inside the .app directory.
It lists out - 
- The certificates that this app must be signed with
- The udid of the devices that this app can run 
- The entitlements that this app is privileged to

The provisioning profile is always created by apple, from the developer store.
In order to read the contents of the provisioning profile, just run - 
```
security cms -D -i $HOME/Library/MobileDevice/Provisioning\ Profiles/bfe492c7.mobileprovision | less
``` 
or better yet, use vim, which apparently auto-converts it ;)

### What does ipas have to do with signing certificates?
An ipa(or more specifically an .app file) is signed using a signing certificate.

### Relation between provisioning profiles and signing?
Provisioning profiles can contain multiple certificates to run. And you can have multiple provisioning profiles for a certificate[4]. Therefore it's a many-many relationship.
The provisioning profile specifies the list of certificates that it's allowed to run. If the app is signed with a certificate that's not in the provisioning profile, then using that provisioning profile, the app will not run on the device. The certificate here might be valid, but the provisioning profile does not recognize that.[4]

Provisioning profile contains - 
- The certificates that are valid for this application 
- The mobile devices that this application can run on 
- The entitlements(the system permissions) that this app has privileges to

The entitlements data is needs to be in-sync with the provisioning-profile 

### What is app thinning?
The generated ipa is built to run only on a specific device. [1]
This is as opposed to fat binaries, that are equipped to run on all CPU architectures. [5]

### How are certificates different from public-private keys?
A certificate is — very broadly speaking — a public key combined with a lot of additional information that was itself signed by some authority (also called a Certificate Authority, or CA) to state that the information in the certificate is correct [2]

### What does it exactly mean when you say, signing an app?
[incomplete] Signing an app requires both the public and private key (why the private key though?)
"In addition to the certificate with the signed public key in it, we also need the private key. This private key is what you use to sign the binaries with. Without the private key, you cannot use the certificate and public key to sign anything."[2]

You can figure out how a particular ipa is signed by unzipping it and running codesign on it's .app directory
```
$ codesign -vv -d MNAdSDKDemo.app
Executable=/Users/nithin.g/Desktop/Ipas/temo/Payload 2/MNAdSDKDemo.app/MNAdSDKDemo
Identifier=net.media.beta.MNAdSDKDemo
Format=app bundle with Mach-O universal (armv7 arm64)
CodeDirectory v=20200 size=22394 flags=0x0(none) hashes=694+3 location=embedded
Signature size=4730
Authority=iPhone Distribution: BetaCraft Technologies Private Limited
Authority=Apple Worldwide Developer Relations Certification Authority
Authority=Apple Root CA
Signed Time=07-Feb-2018 at 2:15:56 PM
Info.plist entries=37
TeamIdentifier=PF48527554
Sealed Resources version=2 rules=13 files=82
Internal requirements count=1 size=204
```

Apparently you can resign it as well - 
```
codesign -f -s '<YOUR CERTIFICATE>'
```
You can list the certificates that can be used for code-signing, on your machine using -
`security find-identity -v -p codesigning`

Signing an app modifies the executable.[2]

Signing does 2 things 
- Figures out who signed the app
- Acts a checksum to see if the app has been tampered in any way

"On iOS, Neither user nor developer can change them: you need an Apple developer or distribution certificate to run an app on iOS."[2]

### What are mach-O binary files? 
Mach-O is a kernel specific file. Mach is an early kernel, whose variants are the current system kernels in iOS and macOS [3]

## Resources
[1](https://developer.apple.com/library/content/qa/qa1795/_index.html)
[2](https://www.objc.io/issues/17-security/inside-code-signing/)
[3](https://en.wikipedia.org/wiki/Mach-O)
[4](https://www.objc.io/issues/17-security/inside-code-signing/#provisioning-profiles)
[5](https://mentormate.com/blog/security-in-ios-protecting-ipa-file-content/)
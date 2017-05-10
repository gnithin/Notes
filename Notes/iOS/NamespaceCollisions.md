## Namespace collision help when using frameworks

 - There are ways in which 2 different frameworks have exact same names collide - 
 	http://stackoverflow.com/questions/178434/what-is-the-best-way-to-solve-an-objective-c-namespace-collision
 	- The solution is really stupid. I don't think stuff like this should ever be attempted in prod level

 - Whats the difference between dynamic and static frameworks? I've only every heard dynamic and static libraries and frameworks just introducing a bundle - https://www.raywenderlich.com/97014/use-cocoapods-with-swift
 	- There are none - http://stackoverflow.com/a/15331319/1518924

 - How do these guys specify that using cocoapods solves every namespace problem - http://stackoverflow.com/questions/31781301/how-to-resolve-symbol-name-conflict-in-a-cocoa-touch-framework#

 - NOTE: Two letter namespaces are reserved for apple only http://stackoverflow.com/a/15539081/1518924

Using pod packager does this -
When building the framework itself, the dependencies are added a prefix (podName)

pod package links - 
http://www.rubydoc.info/gems/cocoapods-packager/1.1.0/Symbols.mangle_for_pod_dependencies
https://github.com/CocoaPods/cocoapods-packager/blob/7abb5df456f9ddc18c4604cb0b7b8de34c924833/lib/cocoapods-packager/builder.rb#L148

It changes the name to Pod#pod_name_#symbol. 
So essentially, the external dependencies across the file are changed. 
For example, AFNetworking library becomes something like MyPod_AFHTTPRequestOperation

These basically make sure that build doesn't fail. 

Need to try importing a filename with similar mangled name as well.

This is the solution that's used by pod package
http://atastypixel.com/blog/avoiding-duplicate-symbol-issues-when-using-common-utilities-within-a-static-library/

So dependencies shouldn't be a problem, as long as we don't have too many dependencies - 
https://github.com/realm/realm-cocoa/issues/2940

My custom outputs and design
- Print out the mangled output of the classname
I've pasted the output below

- Questions
	- What's this PodsDummy string?
	- Is it only for development pods or something? 
	- Maybe I need to find out how this thing looks when I actually need to run it against a framework


GCC_PREPROCESSOR_DEFINITIONS='$(inherited)
AFAutoPurgingImageCache=PodMNAdSdk_AFAutoPurgingImageCache AFCachedImage=PodMNAdSdk_AFCachedImage AFHTTPSessionManager=PodMNAdSdk_AFHTTPSessionManager AFImageDownloadReceipt=PodMNAdSdk_AFImageDownloadReceipt AFImageDownloader=PodMNAdSdk_AFImageDownloader AFImageDownloaderMergedTask=PodMNAdSdk_AFImageDownloaderMergedTask AFImageDownloaderResponseHandler=PodMNAdSdk_AFImageDownloaderResponseHandler...<Paste>

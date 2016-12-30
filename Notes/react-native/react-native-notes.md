# Some notes on setting up and working with react-native

I am trying react-native for android (I have a ubuntu distro and an android phone).

## Setting it up
I've downloaded the things mentioned [here](https://facebook.github.io/react-native/docs/getting-started.html).
It's a lot of stuff to download to be honest. Just follow them to the letter. Do NOT try to skip things.

Create a project like this - 
```
react-native init AwesomeProject
cd AwesomeProject
```

So I've followed all the instructions and connected by device to the machine and tried running `react-native run-android`, it started downloading things again.

An error came up instantly - 
```
./adb: cannot execute binary file: Exec format error
```
I guess my Android installation was not correct (I run a ubuntu 32 bit OS).
[This](http://askubuntu.com/a/710504/362872) answer from askubuntu basically reinstalled the `adb` and I ran `react-native run-android` again :fingers-crossed:

After sometime, a huge wall of red text came up -

```
ERROR  A non-recoverable condition has triggered.  Watchman needs your help!
The triggering condition was at timestamp=1480530541: inotify-add-watch(/home/kamehameha/myspace/react-native-project/AwesomeProject/node_modules/babel-jest/node_modules/babel-core/node_modules/babel-generator/node_modules/detect-indent/node_modules/repeating) -> The user limit on the total number of inotify watches was reached; increase the fs.inotify.max_user_watches sysctl
All requests will continue to fail with this message until you resolve
the underlying problem.  You will find more information on fixing this at
https://facebook.github.io/watchman/docs/troubleshooting.html#poison-inotify-add-watch
```

Turns out `watchman`, which is supposed to help for detecting changes in the filesystem (therefore, I assumed, help with reloading the app on a new change), is raising errors.
[This](https://github.com/facebook/react-native/issues/3199#issuecomment-145426578) solution worked.

So again we I start `react-native run-android`. It completes this time!. Finally some activity on my phone! I see a Red screen with the letters -`Could not get BatchedBridge`.
One more round of googling.

Turns out that I have to do a couple of more things in order for it to run on the device.

So from the solutions listed in [this stackoverflow answer](http://stackoverflow.com/a/38874952/1518924) and [this from the react-native page](), here's what has worked for me - 
```
cd AwesomeProject
mkdir android/app/src/main/assets
react-native start > /dev/null 2>&1 &  
curl "http://localhost:8081/index.android.bundle?platform=android" -o "android/app/src/main/assets/index.android.bundle"

# Note that I am not completely sure that the above was totally necessary. I found that at first.
# This has to keep running 
react-native start > /dev/null 2>&1 &

# This is for the USB device
adb reverse tcp:8081 tcp:8081
```

So after this, I ran the `react-native run-android`, and it finally worked! A `Welcome to React Native!` message loomed on my screen.

Apparently in android devices, to reload the thing, we need to shake the device to get the developer options modal.

I tried `Live Reload`, it works sometimes, sometimes it doesn't. Wish there was a command that I could run from the terminal that just reloads it. Maybe there is one, not able to find it.

 
## Running react-native

### Helpful things when running react-native in vim
- The default template that the `index.android.js` comes up has a tabspace of 2. It uses spaces. Something like this in your `nvim/init.vim` would help - 
  ```
  autocmd filetype javascript setlocal tabstop=8 softtabstop=0 expandtab shiftwidth=2 smarttab
  ```
  Be warned, this is going to affect all the javascript files. I do this since I don't use javascript at all :p. There would be a better way. Something like detecting android.js in the file name and then `autocmd`ing that. I dunno. 


### Helpful stuff 
- Organisation of the react-native code. [This](https://medium.com/the-react-native-log/organizing-a-react-native-project-9514dfadaa0#.adaw2gdr0) blog talks about it very well.
- Helpful tip for using absolute paths in react-native. [Use name value](https://medium.com/@davidjwoody/how-to-use-absolute-paths-in-react-native-6b06ae3f65d1#.1xvuq3e61) in package.json

TODO: 
- Learn flexbox. It seems really simple, but shits not working whatever I do. Go for a tutorial or something.

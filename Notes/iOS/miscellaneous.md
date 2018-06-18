# Miscellaneous iOS stuff 

### WWDC demos 
- [Demo 1](https://developer.apple.com/videos/play/wwdc2018/412/)
- [Demo 2](https://developer.apple.com/videos/play/wwdc2018/416)
- Try to debug without actually re-loading/compiling the app
- Use nscache over NSMutable dictionary
    - Nscache auto-deallocates entries from cache if resources are getting critical
- Memory footprint is dirty and compressed pages.
- Use memory-graphs to get memory information
    - Then pass that to subsequent tools which can perform the analysis for you
- Understand paging
    - Dirty, clean and compressed
- Memory mapped file - A file in the disk that is currently loaded onto memory (into a page more accurately I guess)

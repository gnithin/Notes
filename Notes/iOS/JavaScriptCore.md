Javascriptcore 

## Links
- [NSHipster](http://nshipster.com/javascriptcore/)
- [Raywenderlich](https://www.raywenderlich.com/124075/javascriptcore-tutorial)
- It doesn't support `xmlHttpRequest` apparently
- `JSVirtualMachine` 
    - It's like a sandboxed container. It will not communicate with another vm
    - It will be single-threaded instance
    - It can handle multiple JSContexts though
- `JSContext` 
    - It's the window object equivalent
    - Objects can be passed between different contexts, but they both must be inside the same vm 
- `JSValue`
    - This is the actual data value
- React Native is written on top of this

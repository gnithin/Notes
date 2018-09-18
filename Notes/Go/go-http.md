Golang Http flow works this way - 

- http.ListenAndServe(port, Handler Object)
- Handler is an interface - 
```
func serveHttp(resp,req){
	...
}
```
- This is the very basic stuff that is involved


- Now there are wrappers around serverHttp which do clever things and make it easier for the programmer
- http.HandlerFunc(func(resp, req){}) -> Creates a Handler instance without us having to implement the interface in a separate type 
```
h := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "hello, you've hit %s\n", r.URL.Path)
})

err := http.ListenAndServe(":9999", h)
```
- For performing different logic for different endpoints, serveHttp needs a switch case. Instead use a mux.
```
h := http.NewServeMux()

h.HandleFunc("/foo", func(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, you hit foo!")
})

h.HandleFunc("/bar", func(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, you hit bar!")
})

h.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(404)
	fmt.Fprintln(w, "You're lost, go home")
})

err := http.ListenAndServe(":9999", h)
```

- Middlewares are wrapper-handlers around http.Handler


# References - 
- https://cryptic.io/go-http/
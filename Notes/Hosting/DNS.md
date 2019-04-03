# Understanding DNS 
- DNS servers are basically databases that contain IP to host mapping. That's it fundamentally. It is very elaborate owing to the enormity of requests it handles, settings/configuration it offers and efficiency it needs to provide.
- Domains are bought from registrars, who have the infrastructure for creating and maintaining their own DNS servers.
- A DNS server that contains the IP to host mapping for a specific host is called the start of authority (SOA). Over time, the results from looking up hosts at the SOA will propagate to other DNS servers, which in turn propagate to other DNS servers, and so on, a host will be available across the internet [[1]]
- At the very top of the DNS servers, sits the root-name-server. The root-name-server contains the addresses for top-level-domain root-servers. [[2]]
- Every top level domain root server contains the details of SOA for every hostname in it's domain.
	```
	This great web of DNS servers includes the root name servers, which start at the top of the domain hierarchy for a given top-level domain. There are hundreds of root name servers to choose from for each top-level domain. Though DNS lookups don't have to start at a root name server, they can contact a root name server as a last resort to help track down the SOA for a domain.
	```[[1]]
- So riddikulus.tech (my domain), will have the original name-server information in a DNS-server operated by the vendor(called registrars). This will be a SOA. The location of this SOA will be registered/stored/updated into the TLD root-name servers of .tech, which in turn will have it's info in the root-name-servers.
- Using the DNS servers from your registrar or hosting company means that you have a parked domain. This means that someone else owns the computer hardware for the DNS servers, and your domain is just part of that company's larger DNS configuration
    - By this definition, most of the domain names are basically parked domain names
- DNS servers that are maintained by ISPs are intermediataries. They cache most frequently used domain-names in their db. If not found, they request if from neighbouring servers.
- Each of the DNS servers contain settings which is present in something called the zone file. Each configuration/setting is called a record. There are different types of records

## Different types of records
- Records individual entries inside zone files
-  CNAME, A and AAAA records, These are types of records.
- A Type -> Host type. Domain name host to ip-address, one to one mapping. This is only for IPV4. AAAA type is IPV6.
- Canonical Name (CNAME) — This is an alias for an entry in the sub-domain. Anyone accessing that alias will be automatically directed to the server indicated in the A record.
    - For example - 
        ```
        server1     IN  A       111.111.111.111
        www         IN  CNAME   server1
        ```
- NS -> Nameserver. It means that the current DNS is the SOA for the domain. In case you'd want to use an intermediatary service like Cloudflare(for CDN and DDOS protection), you need to add Cloudflare's name-servers in this entry.

## Questions
- What's the difference between the name-server and the A-type(host) records? They both seem to be doing the same thing?
    - A name server is a computer designated to translate domain names into IP addresses [[2]].
    - Zone files reside in name servers and generally define the resources available under a specific domain, or the place that one can go to get that information.
    - But apart from this, there is also a NS record. 
    - ```
    You may be wondering, "if the zone file resides on the name server, why does it need to reference itself?". Part of what makes DNS so successful is its multiple levels of caching. One reason for defining name servers within the zone file is that the zone file may be actually being served from a cached copy on another name server.
    ```[[2]]

- Which system call is used to resolve the hostname?
    - `gethostbyname` is used when creating a socket connection
    - Whenever a resolution is required, the first thing that is checked is the hosts file. If the ip-address for a given url exists, it is returned
    - If there is no entry in the hosts file, then the url is forwarded to the DNS lookup resolver ip (configured in the machine, usually the ISPs or something big like Google), which communicates with various DNS servers and responds back with IP address if available.

- Why is www such a special sub-domain name?
    - www is just a sub-domain like any-other

[1]: https://computer.howstuffworks.com/dns3.htm
[2]: https://www.digitalocean.com/community/tutorials/an-introduction-to-dns-terminology-components-and-concepts
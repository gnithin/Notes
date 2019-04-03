# Hosting firebase app with custom domain using cloudflare

## Steps 
- Setup your custom domain to point it's nameservers to cloud-flare
- Add the custom-domain into hosting in firebase
- Add the TXT in cloudflare
- Copy the A records from firebase dashboard into cloudflare
	- Make sure that the A records pass through cloudflare (this is because it messes up with verification)
- Wait and cross your fingers for around a day (it really does take some time to get reflected)

## Tools
- Getting the TXT records for a domain 
  ```
  dig -t txt +short riddikulus.tech
  ```
- Getting nameserver details 
  ```
  whois riddikulus.tech
  ```

## Advantages 
- Acts as a CDN
- Automatically detects and handles DDOS
- Has provision to allow some delay for prolonged DDOS attacks
- If your server goes down, Cloudflare will serve your website’s static pages from our cache
	- This is supremely useful
- Purge cache with a single click 
- Can add upto 3 page rules
- Adds IP geo-location (CF-IPCountry)


## Problems 
- https://stackoverflow.com/questions/46776551/rate-limiting-on-firebase-hosting
- https://stackoverflow.com/a/50500357/1518924
- https://stackoverflow.com/a/46776772/1518924
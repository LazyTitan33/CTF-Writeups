# rfc-meta

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0573398e-37cc-4e52-a859-5e3723bb77e6)

# Solution

When accessing the generated web service we just get an OK on a /home page:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/20fa10f7-eec3-47b4-9af2-70548b30926f)

After proxying all the traffic through Burp Suite, we can see it is actually doing several redirects until it lands on `/home`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5f2419dc-c15b-4cc6-9377-5fcd552aa4ce)

A closer look in the response and we can see some hex data.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d6a834e7-e642-46d9-8b53-639734023622)

Instead of manually going through all 15 redirects in order and copy the hex data we can script it to get the flag:  

```python3
import requests

response = requests.get('http://35.234.88.19:31765')

if response.history:
    for resp in response.history:
        hex_flag = resp.reason.replace('MOVED PERMANENTLY','')
        flag = bytes.fromhex(hex_flag).decode().strip()
        print(flag, end='')
else:
    print("No redirects occurred.")
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a320db65-73c5-4d02-836d-b0f4c1bb746a)

`CTF{5ba73b7f830badc3e9d32e85bcdcc172bc417afbabc92ea7a343bc3b79fd722e4c44c}`

Note: This was a nice and easy challenge relying on attention to detail and not relying strictly on the web browser which, in my opinion, you shouldn't do when web hacking anyway.
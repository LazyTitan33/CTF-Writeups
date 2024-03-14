# LockTalk

## Enumeration
In this challenge we get a simple looking API:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d7dcaf62-a1f2-425b-888d-43c92d50327d)

However, trying to get a ticket is blocked by the HAProxy:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/23ad7ddf-b97d-4395-8564-b789b37ad38b)

This can be observed in the provided source code:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8160759c-2e3c-47bc-a878-846719a15d68)

From the source code, we can also see it using a python_jwt library version 3.3.3:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1f194dd1-7c7c-45e4-aa13-348b7f6d6b2c)  
With a bit of googling we can find that it is vulnerable and we should be able to forge new claims:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/455650fc-47d4-445d-bd39-7c504e00cec9)

There's even a helpful [POC](https://github.com/user0x1337/CVE-2022-39227):  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b9a745ac-37eb-4aa1-b232-39fe527b965a)

And we know we need to forge an administrator token from the source code. This is important because usually you would think we need `admin`, but in this case we need `administrator`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cdb31685-2e33-4364-a753-ce16a8ee81d3)

## Solution
Before we forge an administrator token we need a guest token. A bit of researching into HAProxy and bypasses, we find a helpful list here:  
[https://github.com/GrrrDog/weird_proxies/blob/master/Haproxy-and-Nuster.md#vulnerable-configs](https://github.com/GrrrDog/weird_proxies/blob/master/Haproxy-and-Nuster.md#vulnerable-configs)

With a simple extra slash at the beginning of the URL we bypass the proxy and get a token:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a9454257-23ec-43cf-ac0c-52a51a4c9016)

We run the [POC](https://github.com/user0x1337/CVE-2022-39227) we downloaded earlier to forge an administrator JWT token.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/31fb72db-65f4-4fe5-b83c-cfac4d733db6)

We verify and confirm that the administrator claim has been injected:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d27c208d-b837-458b-a801-76f334ad2379)

And we get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c8f3cfb1-be48-4f60-8586-242336acc6f3)

Or not. The weird part of this CVE is how it treats the JSON objects so we actually need to copy the entire thing, including the curly braces and pass that as the JWT:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1c8b9458-6aa6-452d-a8cf-c44077bb7828)

And now we get our flag. Interesting find for this [CVE](https://github.com/advisories/GHSA-5p8v-58qm-c7fp), very strange behaviour:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1fae6111-51e8-4470-8ceb-3a3b618d48f1)

`HTB{h4Pr0Xy_n3v3r_D1s@pp01n4s}`

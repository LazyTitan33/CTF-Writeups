# MFAtigue

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/51500841-d97d-4a44-8663-a7052d379ce6)

### Solution
The provided zip file contains a SYSTEM file and ntds.dit which we can extract hashes from using `secretsdump.py`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c10361ad-f4ab-4a85-afa0-8f6720bd0222)

We feed all those NTLM hashes to hashcat and we have one cracked:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d23f92e9-b4ac-468d-8102-e77984e28530)

It is the hash for user Jillian Dotson:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a8920efb-ea67-442e-b7b1-3fb19376ac96)

When we try to log in:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/122e686a-6b90-4a34-87b9-c11f393326d4)

We get this error message:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/548919c5-2066-4dc9-a4de-3d36d53a79d4)

So we need to make sure we use the correct domain as it is indicating to us and then we get logged in:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a2745d95-f42c-45e2-98ea-359b2cdd5c42)

Or so we think, we are required to approve our sign in request.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bd656b15-25bf-4e74-ab42-4d9c142cbc00)

After we click on Send Push Notification, we see a little notification in the right corner that says it was sent:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/473d7240-f8bf-4c44-8b72-980c30f13afa)

Intercepting with BurpSuite we can see a POST request was made to the /mfa endpoint and a Flask cookie was assigned:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/851ade34-2ceb-46a9-89b0-d9d9a2dd5843)

Using `flask-unsign` we can see it is mentioning a counter:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6b8a1fe1-bb05-4634-bd80-44dc0389eab4)

If we push the button to send a push notification suficient times, 30 to be exact, it will assign this cookie:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f1fca874-f62b-42f6-b6ce-3c3e2d765f37)

And we get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5727dead-411a-4dfc-a4a0-3402c2c2efe6)

flag{9b896a677de35d7dfa715a05c25ef89e}

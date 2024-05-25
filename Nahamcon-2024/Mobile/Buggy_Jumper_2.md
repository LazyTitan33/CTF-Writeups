## Buggy Jumper 2

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5e88825a-1040-4256-bd41-935bde3913cc)

## Enumeration

I used [this](https://appetize.io/) website, made an account with a 10 minute mail and ran the app. It's a cute little game with a bug and two options, to play and shop:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f22eaf14-2451-413e-b5f2-9896a88d3f5d)

The game is fun but not winnable:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5fc0db29-ff4a-454b-83fe-7d821e223c35)

We need way too many points to be able to afford the "drip":  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c6d576c8-b8cc-4948-9c4b-105a6be53ebf)

Looking through the network logs, we can see it making some requests to a specific IP with the Godot User Agent:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b867e53d-965b-4d68-a5e8-e9375ad95539)

When we lose and get 0 points, it saves a null value and uses an authentication header:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/02c39b3a-c758-45a7-a4bb-cd21db84369c)

If we try to buy the drip, it again sends an authenticated request with 0 value:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/75b5f186-fbc9-4d0a-a856-916d864e2d22)

## Solution

Knowing now how the application works, we can replicate it in Burp Suite and send some requests ourselves. We start by telling it how big of a score we got:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f560e33-8eff-4341-9bc2-49491ae4fd16)

Now that we have a sufficient amount of points, we purchase the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4b14e8b9-2879-410c-997c-cac72dcb28d7)

`flag{a31e44ba4df9789ed5491dc43fa22de3}`

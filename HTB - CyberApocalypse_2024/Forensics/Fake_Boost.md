# Fake Boost

## Enumeration
For this challenge, we have a wireshark capture to deal with:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0417d006-1441-4df0-83ec-a4fc90d2f656)

Usually, the first thing I do with wireshark captures is go to `Statistics` -> `Protocol Hierarchy` to see what protocols I'm dealing with, how much data each has etc:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/82704358-4984-48f1-b218-4cc7f4e96016)

We can notice some TCP traffic so let's start following that.

## Solution

On the 3rd TCP Stream, we see a large Base64 blob:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bc812ecb-dd64-4ecb-ae7a-7d331db0d785)

A bit further down, we can see it is reversing and then decoding it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/408a9ffc-621f-473e-bc63-1e5dd4ad4c35)

We do that ourselves in Cyberchef and scroll down a bunch until we find part1 of the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ccc34fbd-c681-40db-907d-56ccde8acde7)

Decoded it in the terminal and set it aside until we find the rest:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/084a63a3-c8e4-4f24-9c1e-566c0509c76c)

Looking through the rest of the script, we can see an Encryption function:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/39926721-63c8-4807-9b76-7f88892b7ccf)

Several AES modes are available but CBC is first in the list:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/511f2bd6-5dba-4ceb-8d72-85b229231dc3)

And also a hardcoded AES key:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6922149c-2216-449d-ad14-858fe28e24ea)

```text
AES Key: Y1dwaHJOVGs5d2dXWjkzdDE5amF5cW5sYUR1SWVGS2k=
```

Towards the end of the wireshark capture, we notice another Base64 blob but no other options. Unlike the previous one, this doesn't seem reversed nor can we simply decode it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1504dd9e-6249-43af-ad94-ca6454d93147)

This must be where the previous encryption we found comes into play. Because only the Key is passed to the encryption function, we can reuse it as the IV and pass these to Cyberchef and decode then decrypt the Base64 blob:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/70d1da07-6cd7-4329-8b53-013bcc66f656)

Weird, this doesn't look like an email address, in fact, it looks Base64 encoded:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/79e6c521-cc21-4c00-859f-edf0ca8ddf2d)

So we decode it and get our second part of the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4ecdc564-b137-4472-930e-890a57f3eae6)

`HTB{fr33_N17r0G3n_3xp053d!_b3W4r3_0f_T00_g00d_2_b3_7ru3_0ff3r5}`

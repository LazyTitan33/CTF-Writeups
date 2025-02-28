# An Offset Among Friends
![image](https://github.com/user-attachments/assets/dc432c53-3950-4573-b8ff-bab7926bed2e)

Attachment: [an-offset](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/an-offset)

## Writeup

A quick decompiling in [dogbolt](https://dogbolt.org/) and we can see what looks like a jumbled flag:  

![image](https://github.com/user-attachments/assets/c0a1c737-10c7-4cde-a36d-f57f26fea2a8)

I recognize this as being rotated, but unlike ROT13, the special characters of curly braces are rotated as well so we can use ROT47 from Cyberchef:  

![image](https://github.com/user-attachments/assets/ff5263da-ee8a-4adf-939d-139dc1891754)

https://gchq.github.io/CyberChef/#recipe=ROT47(-1)&input=Z21iaHxkNjU0MjY1OTM2NDJkMjJiODdiZmJiOTM5ZjU0OTE4ZH4&oeol=VT

flag{c54315482531c11a76aeaa828e43807c}

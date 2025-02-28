# Either Or
![image](https://github.com/user-attachments/assets/bdc998cf-a53e-443a-beab-99366b66fb82)

Attachment: [either-or](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/either-or)

## Writeup

I decompiled this quickly in [dogbolt](https://dogbolt.org/) and saw a string the main function that I recognized to be rotated. Specifically ROT13. 

![image](https://github.com/user-attachments/assets/af444656-be6d-4053-aa0a-3e65e46e7ac3)

Copied the value and rotated it in Cyberchef:  

![image](https://github.com/user-attachments/assets/72609ff9-86ef-4a53-afc3-c77ac8bb3713)

Now that I know the secret password, I give it to the binary and get the flag:  

![image](https://github.com/user-attachments/assets/500c007f-183a-438b-bb1f-36d8cef4c30a)

flag{f074d38932164b278a508df11b5eff89}

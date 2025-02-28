# Math for Me
![image](https://github.com/user-attachments/assets/18e93b6e-2de7-409f-81cb-dee57c13a725)

Attachment: [math4me](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/math4me)

## Writeup

I decompiled the binary and gave the code to chatGPT asking it to solve it for me. Cause I'm lazy.

![image](https://github.com/user-attachments/assets/d06c05e2-c946-4543-ace5-08f6f7e576b3)

This AI is getting better every day. I was surprised to see it was right. I was very sure it is lying to me.

![image](https://github.com/user-attachments/assets/e517f618-b2ab-4c31-b3ee-396465eb89c4)

Another way to get the flag, in a less dumb way, would be to patch the binary, just like I did in [Rock Paper Psychic](https://github.com/LazyTitan33/CTF-Writeups/blob/1c001163cb7482bba6c23b94f5f6e929eb9cda40/Huntress-CTF-2023/Misc/Rock_Paper_Psychic.md) where it is making the check for the special number:  

![image](https://github.com/user-attachments/assets/613d07dd-7f6a-48f6-97fe-59152119bfa9)

Now that I changed the JZ to JNZ, I can pass any value:  

![image](https://github.com/user-attachments/assets/d253f5f0-02c5-400a-93aa-0e4c5e48d00b)

And get the flag:  

![image](https://github.com/user-attachments/assets/320823a7-03b9-4019-87d5-c0f59c08b0b6)

flag{h556cdd`=ag.c53664:45569368391gc}

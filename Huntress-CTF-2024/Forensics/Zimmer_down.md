# Zimmer down

![image](https://github.com/user-attachments/assets/e4c69cf7-37ad-4e59-a5e1-24e850d9caea)

Download: [NTUSER.DAT](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/NTUSER.DAT)

## My Solution

I have parsed NTUSER.dat files before but also a good hint from John when announcing the challenges leads us to use the kali builtin tool called [regripper](https://www.kali.org/tools/regripper/):  

![image](https://github.com/user-attachments/assets/2debf0ae-0b9b-4b97-bf7a-ccf26c0c45ee)


```bash
regripper -r NTUSER.DAT -a
```

We can see a lot of data:  

![image](https://github.com/user-attachments/assets/44e899f8-c66f-47ed-ae92-77078841e66e)

But somewhere further down, this string drew my attention as it looked like it was a Base64 string.  

![image](https://github.com/user-attachments/assets/21a0f165-40b6-4cab-88e0-d69cad1e6176)

But not quite, the b62 at the end is another clue that this is actually a Base62 encoded string which we can decode using [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Base62('0-9A-Za-z')&input=VkpHU3VFUmdDb1ZobDZtSmcxeDg3ZmFGT1BJcWFjSTNFYnk0b1A1TXlCWUtReTVwYURG) and get the flag:  

![image](https://github.com/user-attachments/assets/693afddf-e9d1-42a9-9818-e79640ec96c7)

`flag{4b676ccc1070be66b1a15dB601c8d500}`

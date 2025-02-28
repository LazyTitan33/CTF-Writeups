# Screaming Crying Throwing up
![image](https://github.com/user-attachments/assets/cd4974a9-4119-49aa-b18e-93328da37cc2)

Attachment: [screaming.bin](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/screaming.bin)

## Writeup

The title of the challenge as well as the description points us to the [scream cipher](https://github.com/matthewpwatkins/scream-cipher). We can use [this](https://scream-cipher.netlify.app/) online tool in order to convert our payload.  

However, it is important to open the file in a proper text editor. When read from a powershell terminal or bash, the strange characters are not outputted correctly and won't decode to our flag. I opened it in Sublime Text:  

![image](https://github.com/user-attachments/assets/ce7243a8-270a-4aa9-8ec5-605018e3e086)

Now I can "translate" it and get the flag:  

![image](https://github.com/user-attachments/assets/42d20707-5bc1-44e8-8db6-e78acd0ac6ef)

flag{edabfbafedcbbfbadcafbdaefdadfaac}

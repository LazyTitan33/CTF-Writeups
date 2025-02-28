# Unfurl
![image](https://github.com/user-attachments/assets/71cefee1-9863-4208-beb9-cfe01ee53cea)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/unfurl.zip)

## Writeup

In the source code I can see that there is a filter for the clientIP to ensure only the localhost would access it:  

![image](https://github.com/user-attachments/assets/891bf57d-9aa6-48e7-b699-c75c8c86bae1)

This would give me command execution but it also means I need to find an SSRF vulnerability. The internal app is also running on a random port but we know the range which would make it easy to enumerate:  

![image](https://github.com/user-attachments/assets/cff1474f-825f-4624-83f0-2843645e5459)

The functionality of the website itself is basically just an SSRF, there is no filter that we need to bypass or anything. I've sent the request to Intruder specifying the port range we want to hit to find the internal app:  

![image](https://github.com/user-attachments/assets/8b86dcb6-4fc5-4aa5-8749-a0593ed7dd18)

I also used grep to find the request that has the flag:  

![image](https://github.com/user-attachments/assets/e8a8eb0f-01c2-4b33-8dd3-b4149db51230)

flag{e1c96ccca8777b15bd0b0c7795d018ed}

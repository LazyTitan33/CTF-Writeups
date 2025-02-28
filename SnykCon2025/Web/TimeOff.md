# TimeOff
![image](https://github.com/user-attachments/assets/42a19e34-1933-4b47-bcfc-0ce53de65ba4)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/timeoff.zip)

## Writeup

This website allows me to make a request for time off. It's a POST request that also allows me to upload a file. However, the file_name parameter is vulnerable to Path Traversal according to the [Snyk](https://docs.snyk.io/scm-ide-and-ci-cd-integrations/snyk-ide-plugins-and-extensions/visual-studio-code-extension) Extension for Visual Studio Code :wink::

![image](https://github.com/user-attachments/assets/5e5cfc48-5281-42fb-9513-98d1c03fdbad)

So I just read the flag from the path indicated in the Dockerfile:  

![image](https://github.com/user-attachments/assets/54298171-30e3-472c-a941-bcb32b7732f1)

The 302 redirect will lead me directly to the flag:  

flag{52948d88ee74b9bdab130c35c88bd406}

# Query Code

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/212398a3-8168-4411-876b-68042c729f49)

### Solution
After we download the file, we can find out it is actually a PNG:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0ded0ea7-c6da-4a66-9511-d76f8cc68076)

We rename the file to give it the .png extension and open it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1b97e82c-e1de-449a-a76f-77c53805a782)

Now that we know this is a QR Code, we can use `zbarimg` to scan it and print out the text in it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e11f0248-6f94-4290-8e4f-9fb1ec46b8d9)

flag{3434cf5dc6a865657ea1ec1cb675ce3b}

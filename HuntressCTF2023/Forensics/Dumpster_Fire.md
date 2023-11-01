# Dumpster Fire

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2481bf41-98db-4c7b-8456-cc394ed1bc06)

### Solution
We seem to have a dump of a Linux filesystem. As always, I start by looking in the folders of the user:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/80f9e908-807a-43ea-80d2-ebc72f2974be)

What draws my attention immediately is the `.mozilla` folder. This guy may have accessed some websites containing flags. We can use the following tool to decrypt a Firefox profile and all of its contents, including stored credentials.

https://github.com/unode/firefox_decrypt

Indeed, when we run the tool and give it the specific profile we want decrypted, we get the flag as part of a password used at some point.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a1ad4009-ec68-451f-9d91-f69e578d152b)

flag{35446041dc161cf5c9c325a3d28af3e3}

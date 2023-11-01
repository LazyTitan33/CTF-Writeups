# Zombie

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d0349306-c955-42cc-ab42-38c618235a16)

This challenge allows us to SSH into a box and we see a script that we can read to better understand what is going on:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7a67c836-0bcd-4302-97c7-682939102ae7)

It seems the user runs tail on the flag and then deletes it. However, the process is still running in the background:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0eb141b1-7ff5-4a8a-b732-6f776a2d7a3b)

Which means we should be able to read its file descriptor by going to `/proc/<pid>/fd`.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/722f45e8-32d7-489f-a903-bce368c4c885)

And indeed, we get the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9b9d1058-380a-4f47-a1a8-c6bf0b110680)

flag{6387e800943b0b468c2622ff858bf744}

# fake-add

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e2619114-d0d7-48d2-aebb-af89464d00a6)

# Solution

We can use [dogbolt](https://dogbolt.org/) to decompile small binaries and with this one, we find some interesting looking bytes in it:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/31c424d8-1b3d-4957-b674-b518a6131aea)

I've copied these locally:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2eb57967-4a73-443f-a553-3c381c1c48bb)

Removed the null bytes:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/27d2ec9d-564d-4575-897b-e2da0f45c3d6)

Added the two HEX strings together and decoded the resulting string in Cyberchef:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bfc2c26e-205c-49bc-ba79-b959f1f7908a)

We get our non-standardly formatted flag, but at least this time, it was mentioned in the challenge description:  

`CTF{th1s_is_ju5T_ADD}`

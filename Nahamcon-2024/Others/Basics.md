## Ring Cycle 1 - Basics

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3fbc2fee-ee13-4896-be1c-bd2f34b66e18)

## Enumeration

This challenge is the first one in the Ring Cycle Challenge Group which is focused on reversing. I'm not much into reverse engineering but I will often take a quick look at the dangling fruits. 

I took the provided binary and uploaded it into [dogbolt](https://dogbolt.org/). I was too lazy to start up ghidra for this so I used this online webservice. It's great for quick and small binaries.

We can already see some hex values that should be interesting:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/485ac12f-383d-4bce-8ca1-b172670e85fb)

The binary is expecting a passphrase from us and it is comparing it with this value. I slapped the values into Cyberchef, swapped endianess and hex decoded it:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4a8bc417-0366-4503-ad3f-855a4817d2a4)

```text
You are ready to start your safe cracking journey
```

## Solution

Gave the passphrase to the binary and got the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b392e689-01fb-425e-b131-450ed23e91f8)

`flag{8562e979f1f754537a4e872cc20a73e8}`

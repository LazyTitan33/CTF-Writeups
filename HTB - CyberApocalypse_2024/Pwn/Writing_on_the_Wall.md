# Writing on the Wall

## Solution 
In this binary, when opened in [Ghidra](https://github.com/NationalSecurityAgency/ghidra), we can see it is assigning `6` bytes to local_le, local_18 is `8` bytes ending in a space and it actually reads just `7` bytes from our input which is local_le. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6ff4f4fa-a08e-4837-b269-8e03000104b1)

This means that when it reads our input, the [strcmp](https://www.programiz.com/cpp-programming/library-function/cstring/strcmp) stops at a null byte and compares it with a null byte. So we can just pass 7 null bytes to the program and the strcmp should be true:

```bash
python -c 'print("\x00"*7)'|nc 94.237.56.26 56996
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/22a78a1c-4d3a-4b10-86b9-867d1a7f4c8c)

`HTB{3v3ryth1ng_15_r34d4bl3}`

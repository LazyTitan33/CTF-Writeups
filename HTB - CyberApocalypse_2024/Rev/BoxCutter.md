# BoxCutter

## Solution 
Trying to run the binary directly, we get an error about a box not being found:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7229bb65-d4e3-49f9-9d8b-73ec41aa0ba7)

If we run it with `strace` however, we can see it is trying to access a file or directory that doesn't exist... because it's our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/72695b07-f8c0-4048-8280-9ccfc2268038)

We can also get it with `strace`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9856733a-c422-4a51-ac9a-42b23f5b4cda)

`HTB{tr4c1ng_th3_c4ll5}`

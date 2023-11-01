# Opposable Thumbs

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e3756d2b-5c4f-4da7-8099-e22eed4c170a)

### Solution
In this case, running a file command doesn't really help as we only get that it contains data:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/17f6b37a-80e3-49f6-b8aa-f460ca6c7e08)

In such cases, I revert to manually looking at the file header using a hexeditor. In some cases it may simply be wrong or missing. In this case however, we see an unfamiliar header called `CMMM`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b8bc15e0-ba8d-45aa-89ac-b2412f5f95ed)

A quick google search indicates that this is a Windows cache file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ded9416e-b852-4489-beef-baf646f80ed6)

I'm sure that there are several ways of reading this file, however, the way I did it is by using this tool:  
https://github.com/dbrant/ThumbCacheViewer

This tool sees the other cache files in my VM as well but the one we are interested in is the one with 256 in the name and we get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d27defba-2730-492a-8002-90a3a7057674)

flag{human_after_all}

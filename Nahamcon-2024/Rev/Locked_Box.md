## Locked Box

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a32b2766-4dd3-4f20-8e0a-eb617f212198)

## Solution

This challenge provides us a Makeself self extracting bash script:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1e702c84-c3ac-44b2-b037-eb12c05a8860)

For such scripts, we can carve out the archive itself skipping the first 715 lines because we can see the bytes starting from line 716. 

```bash
 tail -n +715 thebox > archive
```

We confirm that we extracted the archive:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/09dcb410-6efd-4159-a827-1a97ab5b5e44)


The python script from within the archive again contains a lot of flags:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2befbf04-778e-4e76-b391-8b8cb72705db)

But we just need to run it and it will print the flag:  

`flag{3a50c5e41a1c3eee6dcddca9e04992e0}`

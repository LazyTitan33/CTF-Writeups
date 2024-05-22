### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f0b554a7-c2f9-42c5-a252-059b38d1c954)

## Solution

The challenge provides a .bin file that linux can't identify, it just says it's data:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/86b70abc-a829-45b9-805a-38c2829c656f)

But the challenge description does say it's a firmware dump so we are not starting blindly. A good resource as always is [Hacktricks](https://book.hacktricks.xyz/hardware-physical-access/firmware-analysis#analyzing-firmware).

Running `binwalk` on it, we find the `squashfs` filesystem and its `offset`. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1f31a86d-059c-475f-b8b9-0e7a84cf7a3f)

We can use it to carve out the image from the firmware:  

```bash
dd if=chal_router_dump.bin bs=1 skip=4375240 of=dir.squashfs
```

Or you can just let binwalk do it as well:

```bash
binwalk -ve chal_router_dump.bin
```

Using binwalk is definitely the easier method as it gives you all the content you need and the squashfs filesystem is neatly placed in a folder:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/be26b08b-cb9c-4071-b1a6-fa01f5d8306a)

#### Question 1: 
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c00fc784-bb19-41b3-9db3-5468068143eb)

The answer to this one can be found within the squashfs filesystem in `etc/openwrt_release`.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e1b20f7c-22b0-4e09-8ec4-d7cef177f6e2)

#### Question 2:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9719c74d-d3c2-4cb8-a2d9-58bb63fa99cd)  
There are many ways to find this answer, a quick one is using strings and grep:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/df741b73-3def-4ea0-b2aa-486a88b265b0)

#### Question 3:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3ceed161-5425-4b3c-b500-1cba16b9739f)

Sadly this hash can't be found where you would normally expect it to be, in /etc/shadow in the squashfs filesystem. It is actually in the `jffs2` filesystem that was also extracted by binwalk earlier and a folder already created with the content we need:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fd75fe86-136d-49bb-b818-3cb73fda36fc)

In the `upper` directory we can find an archive:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7a84f922-a58b-4121-bee4-53661c2752dd)

When decompressed we can see it also has shadow file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4ab59c7f-c1e7-4d57-b494-a09c79a9eee5)

This is where we find our answer:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f6fef20b-d20a-43a4-9c8f-2bbe2a5ea3e7)

#### Question 4+5:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/444c7f92-366d-4e3d-bc7d-30c2565de621)

The answers can be found in the same folder where we decompressed the archive, in the `etc/config/network` file.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12c19166-c677-42bd-b4ce-9c1d53c00054)

#### Question 6+7:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0398b7fc-da56-404f-81c6-4682facee9a2)

Both answers can be found in `etc/config/wireless`.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d2b26b20-70b1-432e-a551-f35ae7fdd806)

#### Question 8:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5d7b8494-324b-41ab-8e0b-0eacee0158ac)

The last information can be found in `etc/config/firewall`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b265e3f5-290c-4180-b462-087b2675d6d3)

`HTB{Y0u'v3_m4st3r3d_0p3nWRT_d4t4_3xtr4ct10n!!_af640eb12f2108e34ea9f6cc49a018fb}`



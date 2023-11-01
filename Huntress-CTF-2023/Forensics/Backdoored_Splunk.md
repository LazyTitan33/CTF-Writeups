# Backdoored Splunk

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5e917244-7df1-44ff-92ac-90dc5ae7d2ab)

### Solution
There were a lot of files in this archive but one particular one drew my attention, `nt6-health.ps1`. It didn't take me long to find because I was thinking like an attacker and prioritized looking at the scripts first.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7b8402b6-fe2d-4856-9e8b-3494dcbcaa8e)

In this script, we can see an Invoke-WebRequest is made with a specific value for a Basic authorization....  We can replicate that using curl:  

```bash
curl -s -H 'Authorization: Basic YmFja2Rvb3I6dXNlX3RoaXNfdG9fYXV0aGVudGljYXRlX3dpdGhfdGhlX2RlcGxveWVkX2h0dHBfc2VydmVyCg==' http://chal.ctf.games:31029
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b8e3d1ae-fc89-49ec-93a9-ea57108b8ddc)

We can go one step further and carve out the flag directly:  

```bash
curl -s -H 'Authorization: Basic YmFja2Rvb3I6dXNlX3RoaXNfdG9fYXV0aGVudGljYXRlX3dpdGhfdGhlX2RlcGxveWVkX2h0dHBfc2VydmVyCg==' http://chal.ctf.games:32337|awk '{print $2}'|base64 -d
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/30be457d-441e-4698-9efb-98f357f40198)

flag{60bb3bfaf703e0fa36730ab70e115bd7}

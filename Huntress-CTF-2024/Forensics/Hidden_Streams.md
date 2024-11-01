# Hidden Streams


![image](https://github.com/user-attachments/assets/cd2f27da-cee4-4c96-acef-0af076b411a2)

Download: [Challenge.zip](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/challenge-hidden-streams.zip)

## My Solution

I'm sure that there are better ways to do this challenge however, what I usually do is I convert the `.evtx` files to something that is human readable. For this purpose I used the [EvtxECmd.exe](https://github.com/EricZimmerman/evtx) tool to convert the files to `.csv`.  

```bash
.\EvtxECmd.exe -f C:\windows\tasks\Sysmon.evtx --csv c:\windows\tasks --csvf system.csv
```

I looked for powershell commands to see if any were used:  

![image](https://github.com/user-attachments/assets/333b500d-1fc4-4a00-aaec-e485b2bf4395)

We can see a base64 string in a result so we just decode it and get the flag.

```bash
echo 'ZmxhZ3tiZmVmYjg5MTE4MzAzMmY0NGZhOTNkMGM3YmQ0MGRhOX0='|base64 -d
```
                                       
`flag{bfefb891183032f44fa93d0c7bd40da9}`

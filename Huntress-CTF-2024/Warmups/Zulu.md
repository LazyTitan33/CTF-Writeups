# Zulu

![image](https://github.com/user-attachments/assets/8587e755-ff3d-48d1-aa5f-26b63b36394d)

Download: [zulu](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/zulu)

## My Solution

The provided file seems to be a `compress'd data 16 bits`

![image](https://github.com/user-attachments/assets/6fe8b098-feef-498e-8f6d-90a5be2388ca)

A quick google search indicates that this should be a `.z` compressed file:  

![image](https://github.com/user-attachments/assets/5e614f3f-0ef9-4482-9a2b-510dd9a08a6c)

Within the stackoverflow post, we can see how to decompress such files as well:  

![image](https://github.com/user-attachments/assets/13256440-a394-4522-ac40-3a0950361bfd)

So we rename it accordingly, use `uncompress` command to decompress it and get our flag:  

```bash
mv zulu zulu.z
uncompress zulu.z
cat zulu
```

`flag{74235a9216ee609538022e6689b4de5c}`

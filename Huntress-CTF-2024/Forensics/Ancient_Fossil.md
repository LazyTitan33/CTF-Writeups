# Ancient Fossil

![image](https://github.com/user-attachments/assets/3255f8ce-5291-4651-abdb-3d3625ff1c01)

Download: [ancient.fossil](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/ancient.fossil)

## My Solution

This file looks to be a Sqlite3 database based on the header. There were a few different things in it like this rebuild hash for for instance:  

![image](https://github.com/user-attachments/assets/409bfeca-5f3c-467d-98df-3a68fda331d4)

I didn't know what that is so I googled it:  

![image](https://github.com/user-attachments/assets/1e9d919c-fc00-47a1-aeb0-03e762e71376)

It seems that this is part of something called [fossil-scm](https://fossil-scm.org/home/uv/download.html). There are a few things this tool can do, including seeing a .fossil file as a git repo and allowing us to export it:  

```bash
./fossil export --git ancient.fossil|grep flag
```

I did so while grepping for the flag and found it.

`flag{2ed33f365669ea9f10b1a4ea4566fe8c}`

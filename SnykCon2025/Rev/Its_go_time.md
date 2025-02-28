# It's Go Time
![image](https://github.com/user-attachments/assets/62c08e20-9101-4e3c-a039-b4726c08ef6e)

Attachment: [its-go-time](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/its-go-time)

## Writeup

When running this app, it's asking for a 16 byte key:  

![image](https://github.com/user-attachments/assets/664f88e6-51d1-4610-925c-cf0116ace059)

When giving it 16 bytes, it shows error "Invalid Key!":  

![image](https://github.com/user-attachments/assets/2d2b41a9-d39c-42f0-8c8b-f95e5b153b6b)

I spent a long time looking through this app in IDA and Ghidra. I really have a difficult time dealing with GO binaries. After carefully following the flow, I had finally found the JNZ (Jump not equals) conditional jump to the "Invalid key!" error:  

![image](https://github.com/user-attachments/assets/3f126c9a-425f-4afd-b347-53aa7edf857d)

In Ghidra, I went to that address in the binary and patch it by changing the JNZ to JZ (Jump if equals).  The patch works just like I showed in [Rock Paper Psychic](https://github.com/LazyTitan33/CTF-Writeups/blob/1c001163cb7482bba6c23b94f5f6e929eb9cda40/Huntress-CTF-2023/Misc/Rock_Paper_Psychic.md) it's just that here I'm changing a JNZ to a JZ instead of changing the function where a JMP would be.

![image](https://github.com/user-attachments/assets/e4e0f66c-813e-48af-8c3f-3869a4a3fb18)

Now the binary will jump in the other direction and give me the flag:  

![image](https://github.com/user-attachments/assets/050df1dd-e9de-4d80-a03d-b1e64588dc10)

flag{78b229bed60e12514c94e85126b43ec4}

# letters2nums
![image](https://github.com/user-attachments/assets/48bf9194-8a62-40ff-a1e4-2aedc3410d57)

Attachment: [encflag.txt](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/SnykCon2025/attachments/encflag.txt)  [letters2nums.elf](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/letters2nums.elf)

## Writeup

I was doing multiple challenge at the same time at this point and I wasn't very interested in the Rev category so I just copy pasted code from the binary after decompiling it in Ghidra and asked chatGPT what it sees:  

![image](https://github.com/user-attachments/assets/ac3b8c7c-9907-4738-b94c-34fbf6c42a01)

It very nicely gave me working code from the first try:  

```python
with open("encflag.txt", "r") as f:
    encoded_numbers = [int(line.strip()) for line in f.readlines()]

decoded_flag = ""
for num in encoded_numbers:
    char1 = (num >> 8) & 0xFF
    char2 = num & 0xFF
    decoded_flag += chr(char1) + chr(char2)

print("Decoded flag:", decoded_flag)
```

flag{3b050f5a716e51c89e9323baf3a7b73b}

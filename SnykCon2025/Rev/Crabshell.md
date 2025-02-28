# Crabshell
![image](https://github.com/user-attachments/assets/1be269a3-8a48-47e3-acca-4bf157d23daf)

Attachment: [crabshell](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/crabshell)

## Writeup

When running the binary, I can see it is expecting a 16 bytes key:  

![image](https://github.com/user-attachments/assets/4be7c4f8-7deb-4c8a-854b-0b7272491a0c)

Giving it 16 bytes, we get a different error:  

![image](https://github.com/user-attachments/assets/e697f58f-e05b-40fd-a36e-112bff414549)

This is a rust binary so I started with the Main function:  

![image](https://github.com/user-attachments/assets/1816b300-199f-49fd-b371-82c2612cd094)

Going deeper into it, I can see it is making multiple checks on the user input:  

![image](https://github.com/user-attachments/assets/012c0579-043e-42c2-ac8d-a54dadf22b70)

After it checks to ensure it gets 16 bytes, it makes multiple comparisons to see if the input is its valid key.

![image](https://github.com/user-attachments/assets/d6989bbd-5d5b-4d28-bb79-71be863b8c7f)

The first byte it is expecting is `1`. That's `31` in hex. The following 2-8th bytes are `261f2d233117221f` after reversing it to account for the endianness. From the 9th byte we need these values `32136864`. Again reversed because of endianness. The last 3 bytes are `d` = `64` and `h` twice = `68`.

After making these comparisons, there are other MD5 calculations it does however I should have all I need. Putting the entire thing together, I get a 32 bytes MD5 hash which I hex decode and pass to the binary.

```bash
echo -n '31261f2d233117221f32136864646868'|xxd -r -p|./crabshell
```

![image](https://github.com/user-attachments/assets/8601477f-13f7-4ab2-8c1e-1f9e986493f1)

flag{cc811d4486decc3379dd13688a46603f}

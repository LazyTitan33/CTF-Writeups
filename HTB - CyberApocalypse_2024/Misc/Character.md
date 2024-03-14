# Character

## Solution

We connect to the given IP and port and it asks us for an index. Starting from 0 going through 100+ we see that each index contains a letter of the flag.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3cb33ab4-3aac-4dd8-a480-ac05b0be67c1)

But there's too many to do manually:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8e22c62a-ecd6-4e75-b5f1-8e25d5ed35e8)

So I scripted it:  

```python3
from pwn import *

r = remote('83.136.254.199', 30965)

print('H', end='')
r.recvuntil(b': ')
for i in range(104):
	r.sendline(str(i).encode())
	r.recvuntil(b': ')

	flag = r.recvline().decode().strip()[22:]
	flag = flag.replace(' ','')
	flag = flag.replace(':','')
	print(flag, flush=True, end='')
```
![flag](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a520ce6c-eb16-408a-b01b-a38ed8fea6bb)

`HTB{tH15_1s_4_r3aLly_l0nG_fL4g_i_h0p3_f0r_y0Ur_s4k3_tH4t_y0U_sCr1pTEd_tH1s_oR_els3_iT_t0oK_qU1t3_l0ng!!}`

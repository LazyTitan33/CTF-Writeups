# Stop Drop and Roll

## Solution
We connect to the provided IP and port we are given instructions on how to complete the challenge:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0fa1df91-60f1-45b3-8599-717f8f6d1784)

We need to script something that will answer the challenge accordingly. Here's my script that just replaces the words:

```python3
from pwn import *
import warnings
warnings.filterwarnings('ignore')

r = remote('94.237.48.92', 37120)

r.recvuntil(b')')
r.sendline(b'y')
r.recvline()

while True:
	try:
		challenge = r.recvline().decode().strip()
		if 'FIRE' or 'ROLL' or 'PHREAK' in challenge:
			answer = challenge.replace('FIRE','ROLL').replace('PHREAK','DROP').replace('GORGE','STOP').replace(', ','-')
			r.recvuntil(b'? ')
			r.sendline(answer)
		else:
			print(challenge)
	except EOFError:
		print(challenge)
		break
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/aa95cc10-1add-445a-873d-46ff02013db6)

`HTB{1_wiLl_sT0p_dR0p_4nD_r0Ll_mY_w4Y_oUt!}`

This is another challenge where the description is actually helpful:

<i>"The alien species use remote machines for all their computation needs. Pandora managed to hack into one, but broke its functionality in the process. Incoming computation requests need to be calculated and answered rapidly, in order to not alarm the aliens and ultimately pivot to other parts of their network. Not all requests are valid though, and appropriate error messages need to be sent depending on the type of error. Can you buy us some time by correctly responding to the next 500 requests?"</i>

When we use netcat to connect to the service provided by this challenge, we see a Menu. We choose 2 and we get some instructions:

![image](https://user-images.githubusercontent.com/80063008/227538331-35200fea-6f15-4ebf-9ad4-4cad91d58de2.png)

If we use 1 to start the challenge, we start receiving an equation that we need to solve.

![image](https://user-images.githubusercontent.com/80063008/227538596-bd486a83-343d-4c1c-957e-19f85bf8f09c.png)

This is equation number 001. This means we need to solve 500 of these and then we'll get the flag.

As per the Help menu, if we get an equation that is dividing by 0, we need to send `DIV0_ERR` to the server. If we get an invalid syntax we need to send `SYNTAX_ERR` and if we get a result outside the range of -1337 and 1337 we need to send `MEM_ERR`.

This is my python script that does all of that.

```python
#!/usr/bin/python3

from pwn import *

context.log_level = 'info'

io = remote('209.97.134.50', 30935)

io.sendline(b'1')
io.recvuntil(b': ')
result = io.recvline().strip()[:-4]
for i in range(500):
	try:
		rounded_result = eval(result)
		rounded_result = round(rounded_result, 2)
		if rounded_result > 1337.0 or rounded_result < -1337.0:
			io.sendline(b'MEM_ERR')
			if i == 499:
				print(io.recvline().strip().decode())
				break
			result = io.recvline().strip().decode()[9:-4]
		else:
			print(str(i) + ' sending: ' + str(rounded_result))
			io.sendline(str(rounded_result))
			if i == 499:
				print(io.recvline().strip().decode())
				break
			result = io.recvline().strip().decode()[9:-4]
			
	except ZeroDivisionError:
		io.sendline(b'DIV0_ERR')
		if i == 499:
				print(io.recvline().strip().decode())
				break
		result = io.recvline().strip().decode()[9:-4]
	except SyntaxError:
		io.sendline(b'SYNTAX_ERR')
		if i == 499:
			print(io.recvline().strip().decode())
			break
		result = io.recvline().strip().decode()[9:-4]
```

After going through all the equations, we get the flag:  
![image](https://user-images.githubusercontent.com/80063008/227539202-3e3d52c0-fd90-409d-a11a-9446c12b7764.png)

HTB{d1v1d3_bY_Z3r0_3rr0r}

![image](https://user-images.githubusercontent.com/80063008/166420108-f9972d9f-bcc8-48d1-8dee-47d3972d8277.png)

We are first asked to convert from binary to ASCII.

![image](https://user-images.githubusercontent.com/80063008/166420146-595c17e4-5c43-43df-89fa-b04dbc87d073.png)

Then from HEX to ASCII

![image](https://user-images.githubusercontent.com/80063008/166420176-7e54a20d-da7e-4ef7-8e97-39aa0a637bf5.png)

From Octal to ASCII

![image](https://user-images.githubusercontent.com/80063008/166420218-14abfbc2-6016-443a-803b-361cd04318a7.png)

From INT to ASCII

![image](https://user-images.githubusercontent.com/80063008/166420263-89af59d3-8fef-42af-969b-97cdcce19a90.png)

From Base64 to ASCII

![image](https://user-images.githubusercontent.com/80063008/166420292-9a500845-1c3f-4583-ac3a-e794d2e205dc.png)

From little-Endian HEX to Big-Endian ASCII

![image](https://user-images.githubusercontent.com/80063008/166420345-23c79ab4-e2f6-49a5-98df-a8ab422d2aa8.png)

The script below does it for us.

```python3
#!/usr/bin/python3


from pwn import *
import binascii
import base64


context.log_level = 'error'

r = remote('challenge.nahamcon.com', 30960)

r.recvlines(29)
binary_content = r.recvline().decode().strip()
firstAnswer = binascii.unhexlify('%x' % int(binary_content, 2)).decode()
r.recvuntil('=')
r.sendline(firstAnswer)
r.recvlines(2)

hex_content = r.recvline().decode().strip()
secondAnswer = bytes.fromhex(hex_content).decode()
r.recvuntil('=')
r.sendline(secondAnswer)
r.recvlines(3)

octal_content = r.recvline().decode().strip()
thirdAnswer = bytes.fromhex(hex(int(octal_content, 8))[2:]).decode()
r.recvuntil('=')
r.sendline(thirdAnswer)
r.recvlines(3)

int_content = int(r.recvline().decode().strip())
fourthAnswer = bytes.fromhex(hex(int_content)[2:]).decode()
r.recvuntil('=')
r.sendline(fourthAnswer)
r.recvlines(2)

b64_content = r.recvline().decode().strip()
fifthAnswer = base64.b64decode(b64_content).decode()
r.recvuntil('=')
r.sendline(fifthAnswer)
r.recvlines(2)

endian_content = r.recvline().decode().strip()
sixthAnswer = bytes.fromhex(endian_content).decode()[::-1]
r.recvuntil('=')
r.sendline(sixthAnswer)
r.recvuntil(":")
print(r.recvline().decode().strip())
```

![image](https://user-images.githubusercontent.com/80063008/166420536-dd695941-3f28-466c-9f59-7d565bb207df.png)

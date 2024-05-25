## Taking Up Residence

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e0bd965a-613e-49d0-ba76-888cdd4bcf64)

## Solution

For this challenge we just get a file that is only identified as data:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fa639b8c-0243-4924-84f1-1d830a42ff4f)

However, if we look at it with `xxd` we can see a `FILE0` header:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8b20a29-f50a-4685-bb54-d34dfda8c7e6)

A quick google search reminds us that this is an [MFT](https://learn.microsoft.com/en-us/windows/win32/fileio/master-file-table) file:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7b320ad9-054d-4c1f-82b3-aa658dc9e66d)

A very good tool that allows a grafical viewing of the content of such files is the [MFTViewer](https://ericzimmerman.github.io/). It takes a long time for it to load because of its size, but eventually we have it loaded and find a `flag.txt` and `ransom.py` in the Downloads folder:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f5616025-7766-4fb7-85a5-aa89fa4e5615)

In the bottom right, we can see the ASCII data content of the flag.txt file:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c7c0d608-ffe7-4f70-a147-ae3c67eeb1be)

So we'll save this for later:  

```text
gAAAAABmS9s32v5Ju181EaJhh2vYMsR6MJ31SK-9mDwgiCz3_MBWopjqqynjoY_-HNOw3tX1T3RthBZHz9ylmyqckZ0gUZ_6T7UUxprMHoCAaTV3m1q0weznBg98RL7dRVhRn0cX6Xta
```

For the ransom.py we can see 2 data streams:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3958f1b7-28c1-491f-b694-8bfaabc55d18)

Base64 decoding the string in the first data stream we see that it is actually getting the second data stream as the key and using it for a Fernet Encryption:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/10dde406-9790-4002-a623-512cb9e55478)

```python
from cryptography.fernet import Fernet
import subprocess

key = subprocess.run(["powershell", "-EncodedCommand", "RwBlAHQALQBDAG8AbgB0AGUAbgB0ACAALQBQAGEAdABoACAAIgByAGEAbgBzAG8AbQAuAHAAeQAiACAALQBTAHQAcgBlAGEAbQAgACIAawBlAHkAIgA="], capture_output=True, text=True).stdout.strip()

print(key)
with open('flag.txt', 'r') as reader:
    message = reader.read()
f = Fernet(key)

encrypted_message = f.encrypt(message.encode())
print(encrypted_message)
with open('flag.txt', 'w') as writer:
    writer.write(encrypted_message.decode('ascii'))
```
The second data stream is our key to decrypt the flag:  

```text
62QJTO5dH0xaKgmiVfOFKNYCBMfRiNF5L7rxDChc0SU=
```

Armed with this knowledge we can use [CyberChef](https://gchq.github.io/CyberChef/#recipe=Fernet_Decrypt('62QJTO5dH0xaKgmiVfOFKNYCBMfRiNF5L7rxDChc0SU%3D')&input=Z0FBQUFBQm1TOXMzMnY1SnUxODFFYUpoaDJ2WU1zUjZNSjMxU0stOW1Ed2dpQ3ozX01CV29wanFxeW5qb1lfLUhOT3czdFgxVDNSdGhCWkh6OXlsbXlxY2taMGdVWl82VDdVVXhwck1Ib0NBYVRWM20xcTB3ZXpuQmc5OFJMN2RSVmhSbjBjWDZYdGE) to decrypt it and get our flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/98522a9c-c1f1-40b0-aee6-e59239275396)

`flag{a4096cd70d8859d38cf8e7487b4cd0fa}`

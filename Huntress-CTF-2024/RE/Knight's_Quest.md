# Knight's Quest

![image](https://github.com/user-attachments/assets/73505958-f30f-4230-8ba2-f905bfe591ff)

## My Solution

I manually went through the stripped functions from bottom to top in Ghidra until I found this function that seemed to have some hex strings in it and Xoring them.

![image](https://github.com/user-attachments/assets/9f734f1d-b5cf-440f-b741-a0f04602faca)

I had chatGPT spit out a python script to replicate it and got the password which the script also submits to the challenge and gets the flag.

```python
#!/usr/bin/python3

import requests, json

def to_bytes(value):
    """Convert a 64-bit integer to a little-endian byte array."""
    return value.to_bytes(8, byteorder='little')

def xor_and_map():
    # Initialize variables with the given hexadecimal values
    local_250_values = [
        0x446b684155444f42, 0x63374d5a336a4c4d, 
        0x31746c4255396f66, 0x6e4c375942554e41
    ]
    local_230_values = [
        0x384c686770646365, 0x6236734a595a676d, 
        0x657a514d666e6f68, 0x514c344970736a44
    ]

    local_250 = b''.join(to_bytes(value) for value in local_250_values)
    local_230 = b''.join(to_bytes(value) for value in local_230_values)

    result = []

    for i in range(32):
        bVar1 = (local_250[i] ^ local_230[i]) % 0x3e
        bVar6 = bVar1 + 0x41
        if bVar6 > 0x5a:
            if bVar6 < 0x61:
                bVar6 = bVar1 + 0x47
            elif bVar6 > 0x7a:
                bVar6 = bVar1 - 10
        result.append(bVar6)

    return ''.join(chr(b) for b in result)

# Run the function and print the result
password = xor_and_map()


url = 'http://challenge.ctf.games:32676/submit'
data = {"password":password}
r = requests.post(url, json=data)
flag = r.json()
print(flag['flag'])
```

• Endian Conversion: The to_bytes function converts a 64-bit integer to an 8-byte array in little-endian format.  
• Byte Arrays Construction: The local_250 and local_230 values are converted to byte arrays and concatenated.  
• XOR Operation and Mapping: The loop performs the XOR operation and adjusts the result as before, ensuring it falls within the specified ASCII ranges.  
• Result Construction: The resulting bytes are joined into a string and printed.  

The password is: `hmafgAhAalqmQABBOAZtP3OWFegsQDAB`

We send it and get the flag:  
![image](https://github.com/user-attachments/assets/330d8019-cfa2-4f2f-8cc8-567a10743d16)


`flag{40b5b7e5395ee921cbbc804d4350b9c1}`

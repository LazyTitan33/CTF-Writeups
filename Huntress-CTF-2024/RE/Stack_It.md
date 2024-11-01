# Stack It

![image](https://github.com/user-attachments/assets/e69c38e3-23f5-4939-889b-ef7e52a2fe2f)

Download: [stack_it.bin](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/stack_it.bin)

## My Solution

There's a XOR being done between these two values for which we can see the bytes in Ghidra.


![image](https://github.com/user-attachments/assets/f377fdd8-b192-4d39-afcb-e077862a1da6)


Together with chatGPT, we came up with this script that gives us the flag:

```python

extracted_data = [
    0x53, 0x51, 0x51, 0x55, 0x52, 0x5e, 0x56, 0x07,
    0x01, 0x04, 0x0d, 0x02, 0x00, 0x03, 0x56, 0x5b,
    0x0f, 0x50, 0x07, 0x01, 0x53, 0x50, 0x0b, 0x50,
    0x55, 0x00, 0x51, 0x5b, 0x01, 0x06, 0x53, 0x06
]


hash_bytes = [ 
    0x31, 0x65, 0x63, 0x66, 0x66, 0x38, 0x62, 0x65, 
    0x63, 0x65, 0x39, 0x34, 0x38, 0x36, 0x32, 0x38, 
    0x37, 0x64, 0x63, 0x37, 0x36, 0x35, 0x32, 0x31,
    0x61, 0x38, 0x34, 0x62, 0x62, 0x37, 0x63, 0x30]

# XOR the extracted bytes with the hash bytes
flag_bytes = bytearray()

# Iterate over the length of extracted_data
for i in range(len(extracted_data)):
    # Use the modulo operator to wrap around hash_bytes if needed
    flag_bytes.append(extracted_data[i] ^ hash_bytes[i % len(hash_bytes)])

# Add the closing bracket for the flag
flag_bytes.append(0x7d)  # Closing brace '}'

# Construct the full flag string
flag = b'flag{' + flag_bytes

# Print the flag
print(flag.decode())
```

![image](https://github.com/user-attachments/assets/e920453b-063f-4fc7-ad03-1193787d49b0)


`flag{b4234f4bba4685dc84d6ee9a48e9c106}`

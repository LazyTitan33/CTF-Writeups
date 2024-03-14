# BunnyPass

## Solution 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f0797e6e-6b6f-49d8-b5ab-b78b0a276a29)

For this challenge, we are given this script:  

```python3
import socket
import json

def exchange(hex_list, value=0):

    # Configure according to your setup
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 1337        # The port used by the server
    cs=0 # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)
    
    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Serialize data to JSON and send
        s.sendall(json.dumps(command_data).encode('utf-8'))
        
        # Receive and process response
        data = b''
        while True:
            data += s.recv(1024)
            if data.endswith(b']'):
                break
                
        response = json.loads(data.decode('utf-8'))
        #print(f"Received: {response}")
    return response

# Example command
jedec_id = exchange([0x9F], 3)
print(jedec_id)
```
As it is specified in the code comments, this connects to the W25Q128 chip and reads the `jedec_id` from it however, we want to read more than that, we leave the code as is and change the last few lines to read the first 256 bytes from the chip's memory then convert the bytes into characters and put them together, we stop when we found `}` and print the full flag.

```python3
import socket
import json

def exchange(hex_list, value=0):

    # Configure according to your setup
    host = '94.237.49.116'  # The server's hostname or IP address
    port = 39171        # The port used by the server
    cs=0 # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)
    
    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Serialize data to JSON and send
        s.sendall(json.dumps(command_data).encode('utf-8'))
        
        # Receive and process response
        data = b''
        while True:
            data += s.recv(1024)
            if data.endswith(b']'):
                break
                
        response = json.loads(data.decode('utf-8'))
    return response


# Example command
# jedec_id = exchange([0x9F], 3)
data = exchange([0x03, 0x00, 0x00, 0x00], 256)
flag = ''
for i in data:
    flag += chr(i)
    if i == ord('}'):
        break
print(flag)
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/64539953-87fe-4af8-8c1b-9ddb4a6afcdd)

`HTB{m3m02135_57023_53c2375_f02_3v32y0n3_70_533!@}`

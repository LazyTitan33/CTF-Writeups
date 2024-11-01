# Mystery

![image](https://github.com/user-attachments/assets/b03b0809-03c4-412d-aa1c-65f832ad40b5)

## My Solution

This one was puzzling at the beginning but I knew there is enough information in the description to figure out what it is encoded in but I couldn't quite put my finger on it, so I asked ChatGPT.  

![image](https://github.com/user-attachments/assets/0f91c826-068a-4e25-b7d7-7886197c0344)

It mentioned the Enigma machine and gave a python script to decode the message:

```bash
pip3 install py-enigma
```

```python3
from enigma.machine import EnigmaMachine

# Setup Enigma machine with your settings
machine = EnigmaMachine.from_key_sheet(
    rotors='VI I III',
    reflector='B',
    ring_settings='1 1 1',  # Ring settings in the key sheet start from 1 (A = 1)
    plugboard_settings='BQ CR DI EJ KW MT OS PX UZ GH'
)

# Set the initial rotor positions
machine.set_display('AQL')  # Initial rotor positions A, Q, L

# Ciphertext
ciphertext = 'rkenr wozec gtrfl obbur bfgma fkgyq ctkvq zeucz hlvwx yyzat zbvns kgyyd sthmi vsifc ovexl zzdqv slyir nwqoj igxuu kdqgr fdbbd njppc mujyy wwcoy'.replace(' ', '')

# Decrypt the message
plaintext = machine.process_text(ciphertext)

print('Decrypted Message:', plaintext)
```

![image](https://github.com/user-attachments/assets/ecd65168-6a51-4b37-b481-8cc6778fbcce)

`FLAGFDFEABCACBEBFBADAEFBECCAADDDBAFEZZZ`

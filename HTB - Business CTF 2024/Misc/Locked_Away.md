### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/321ae8a7-e8d8-450f-9f62-290288d83cc1)

## Enumeration

We get the source code below for what looks to be a python jail.

```python3
banner = r'''
.____                  __              .___    _____                        
|    |    ____   ____ |  | __ ____   __| _/   /  _  \__  _  _______  ___.__.
|    |   /  _ \_/ ___\|  |/ // __ \ / __ |   /  /_\  \ \/ \/ /\__  \<   |  |
|    |__(  <_> )  \___|    <\  ___// /_/ |  /    |    \     /  / __ \\___  |
|_______ \____/ \___  >__|_ \\___  >____ |  \____|__  /\/\_/  (____  / ____|
        \/          \/     \/    \/     \/          \/             \/\/     
'''


def open_chest():
    with open('flag.txt', 'r') as f:
        print(f.read())


blacklist = [
    'import', 'os', 'sys', 'breakpoint',
    'flag', 'txt', 'read', 'eval', 'exec',
    'dir', 'print', 'subprocess', '[', ']',
    'echo', 'cat', '>', '<', '"', '\'', 'open'
]

print(banner)

while True:
    command = input('The chest lies waiting... ')

    if any(b in command for b in blacklist):
        print('Invalid command!')
        continue

    try:
        exec(command)
    except Exception:
        print('You have been locked away...')
        exit(1337)
```

A lot of things are filtered but ultimately our input is passed to exec function. One thing to note is that the code only exits if there is an exception, otherwise we are still in the same code instance. Furthermore, the word clear and blacklist are not filtered.

## Solution
This means we can issue the command `blacklist.clear()` and it will clear the contents of the blacklist list.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5c0289bc-bfe2-4efe-a1a4-9d5c39dac3c1)

Then, since open is no longer blacklisted, we can simply call the `open_chest()` function:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/86907718-3856-463f-9599-82ada410f2c2)

`HTB{bYp4sSeD_tH3_fIlT3r5?_aLw4Ys_b3_c4RefUL!_3a1b652e405884ac120fc3058d7182a1}`

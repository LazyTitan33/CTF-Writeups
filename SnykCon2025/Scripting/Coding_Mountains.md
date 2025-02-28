# Coding Mountains
![image](https://github.com/user-attachments/assets/000e489e-1db3-4ac0-b4ed-9b511a7a276b)

Attachment: [mountains.json](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/SnykCon2025/attachments/mountains.json)

## Writeup

For this challenge I have to answer 50 questions in quick succession. The questions relate to various mountains and their tallest peak and year of first ascent.

At the time when I solved it, it didn't have an attachment so it was a bit more difficult but way more rewarding when finally getting it done.

For quite a while I tried using wikipedia to carve out the details. This was slow and not very reliable because of the different names given by the challenge and what was found on Wikipedia. I was googling the names of the mountains manually as well trying to find various databases or datasets where I would find them.

Eventually I found [this](https://github.com/mina-pst/web-scrapting/blob/ec76a20e7def4c138ce1af8afc62b4c4cb9ea43a/Highest%20Mountain.csv#L101) csv file which allowed me to be very fast. Using the script below I'm scraping the csv file and searching for the answers. It's not great but running it with pwntools in DEBUG mode, I can see the flag at the end:  


```python
import re
from pwn import *
import warnings
warnings.filterwarnings('ignore')

import csv
import re

def extract_mountain_info(file_path, mountain_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Skip the header row
        next(reader)
        
        for row in reader:
            # row[1] is the Mountain name(s), row[2] is the Height, row[7] is the First ascent
            if mountain_name.lower() in row[1].lower():
                # Extract height in feet from row[2]
                height_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*ft', row[2])
                first_ascent_year = row[7] if row[7] else "none"

                if height_match:
                    height_feet = height_match.group(1).replace(',', '')  # Remove commas
                    return f"{height_feet},{first_ascent_year}"
                else:
                    print("Height information not found.")
                return

        print("Mountain not found in the CSV.")


r = remote('challenge.ctf.games', 32241)
r.recvuntil(b'(Y/n): ')
r.sendline(b'y')

r.recvline()  # This receives the welcome message
while True:
    mountain_prompt = r.recvuntil(b': ').decode().strip()
    match = re.search(r'What is the height and first ascent year of (.+):', mountain_prompt)
    if match:
        mountain_name = match.group(1).strip()  # Extract the mountain name
        r.sendline(extract_mountain_info('mountains.csv',mountain_name))
        r.recvline()
    else:
        print("Mountain name not found.")
```

```bash
python exploit.py DEBUG
```
![image](https://github.com/user-attachments/assets/3f0b77d7-7be5-4806-b2e9-a7d2ebf2b5b0)

I'll leave using the json they provided as an exercise to the reader.

flag{33e043f76c3ba0fe9265749dbe650940}

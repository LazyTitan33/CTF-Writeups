# Makeshift

## Solution 
For this challenge, we get an output.txt and source.py file.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/196697f0-7717-4d2f-9d9d-dbc261bb2504)

The output.txt contains:

```
!?}De!e3d_5n_nipaOw_3eTR3bt4{_THB
```

And the source.py contains the python code:  

```python3
from secret import FLAG

flag = FLAG[::-1]
new_flag = ''

for i in range(0, len(flag), 3):
    new_flag += flag[i+1]
    new_flag += flag[i+2]
    new_flag += flag[i]

print(new_flag)
```
No changes are required here really:  

```python3
flag = '!?}De!e3d_5n_nipaOw_3eTR3bt4{_THB'[::-1]
new_flag = ''

for i in range(0, len(flag), 3):
    new_flag += flag[i+1]
    new_flag += flag[i+2]
    new_flag += flag[i]

print(new_flag)
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/42068fd7-bf7d-4e08-8aac-2d2e856ba934)

`HTB{4_b3tTeR_w3apOn_i5_n3edeD!?!}`

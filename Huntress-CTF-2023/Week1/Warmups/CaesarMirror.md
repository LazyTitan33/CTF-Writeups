# CaesarMirror

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/69d8126e-d28d-45eb-8651-c34a1fce0dbc)

### Solution
Reading the provided file, we see two columns of text:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c1608fea-391c-4139-a6f9-5d33e2932557)

The name of the challenge as well as the way the text looks like, make me thing  of `rot13` so I apply it to the file and get the left column decoded and we get a first part of the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9d4312bb-9a3e-46f4-a35a-94c9a17f327a)

```bash
flag{julius_
```
We use a text editor to carve out only the second column, after we applied the `rot13` and save it separately. If you look closely enough, the last word is Caesar spelled backwards so let's apply `rev` on this column:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/997bd908-1475-47c8-9cd2-a51f170104e6)

It was succesful and we have our 2nd and 3rd part of the flag. Putting it all together we get:

flag{julius_in_a_reflection}

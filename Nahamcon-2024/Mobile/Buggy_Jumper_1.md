## Buggy Jumper 1

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7bef5be1-e407-45a7-a12c-23e54c90b745)

## Enumeration

While looking through the source code, we see multiple mentions of Godot and find this `flag.gdc` file.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8a4179b3-1c98-40cf-a962-cdd2ce9e209b)

But it seems to be a binary file so we can't just read it. I asked ChatGPT for some clarification and it confirmed what I thought:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/68abb4ce-16b8-41ff-af02-0b22b7e4e53d)

We are dealing with a Godot compiled code that we need to decompile. 

## Solution

I found [this](https://github.com/bruvzg/gdsdecomp/releases) great precompiled tool on github. I ran it and opened the `flag.gdc` and selected the lasted bytecode version from the drop down list:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d2be83f2-6b3f-4808-95c8-7fb6eaa55bef)

It decompiled it and now we can read it and get the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f5b4d82-3cd9-445e-9198-79ad84411bfa)

`flag{c2d5a0c9cae9857a3cfa662cd2869835}`

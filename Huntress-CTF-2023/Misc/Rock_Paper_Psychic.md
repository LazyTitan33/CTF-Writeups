# Rock, Paper, Psychic

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/601b0cb5-0937-48d3-9e41-e9b2e9b94802)

### Solution
For this challenge, we get a PE executable. When we first run it, regardless of what we choose, we always lose:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cbb5c325-d679-488d-b0b0-29dc9ce519b8)

The name of the program is interesting. It seems to be a hint for us to patch the program. I've opened it in Ghidra to learn more about what it does and how. At first, we see a function called `determineWinner`   

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7a998d20-8fdf-4610-be06-7baaebce1b7e)

We then we also find a function called `printFlag`   

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/69094df6-6739-4d32-804d-655ec9d01092)

The `determineWinner` function does a few comparisons and if statements determining winner depending on whether the user chooses rock, paper or scissors. I spent some time trying to mess with those and patch the binary to spit out the flag but I didn't find an easy and elegant solution. Then I got an idea. At the end of all of these, the function returns 0:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9e8a0f7f-5963-4737-be44-ba8105206613)

What if we patch that and instead of returning 0, it simply jumps to the `printFlag` function?! So regardless of the if statements, regardless of what the outcome of the `determineWinner` function will be, it will jump where we want to go and print the flag.

We right click on the RET and click on `Patch Instruction`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/99e37f29-1122-4892-aa7d-6a54a2fbc889)

We replace the RET with `JMP` and tell it where to jump:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/af36e524-be1e-407a-9220-9f7eddc7b491)

Hit enter and now the RET has been replaced with our JMP:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cbecf24d-62c1-4ccb-841c-6a01992768f6)

We highlight this part and click on the icon in Ghidra to Display the Script Manager.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/50ee0bf7-9514-4570-a7c2-6a27baedd457)

We find our [SavePatch.py](https://github.com/schlafwandler/ghidra_SavePatch/blob/master/SavePatch.py) script and run it. Because we've highlighted our patched instruction, it automatically determines the size and location it needs to patch.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7fcca990-fe57-4b6b-ba10-c5bee9293f49)

Now we run the binary again and choose anything we want. It beats us but also gives us the flag which we are fine with because we ultimately win:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6046c231-3d79-4c48-bebb-72239b1e80ba)

flag{35bed450ed9ac9fcb3f5f8d547873be9}


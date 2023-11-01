# Comprezz

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4762a806-d48f-4315-8b18-4fed0ac0965b)

### Solution
Running the file command on this, we get a strange message:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/79e0da56-e053-4142-816a-95e67261b563)

A quick Google search seems to indicate this is a `.z` file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5990af18-e103-4a4e-89d3-cc58716b4001)

On this link, we can find this information:  
https://stackoverflow.com/questions/12168081/how-can-i-uncompress-z-file-under-ubuntu
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/20e1be55-4610-4258-80ca-d699fe2353bb)

So let's go ahead and rename the file and try to uncompress it:

```bash
mv comprezz comprezz.z
uncompress comprezz.z
```
It works, and we get a file that we can read:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5b272514-713d-4fc8-b331-02844b6eaab6)

flag{196a71490b7b55c42bf443274f9ff42b}

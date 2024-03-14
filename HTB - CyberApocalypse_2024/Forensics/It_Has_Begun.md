# It Has Begun

## Enumeration
The first very easy forensics challenge provides a bash script:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d8d81baa-34e2-4e65-b225-dab9e13c71d2)

## Solution
Within it, we find the first part of the flag, but reversed:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8183fdf1-d7d0-4ad2-b903-8c35d40d012d)

No worries, we can reverse it back in the terminal using `rev`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2da3e7c4-8dd5-442e-abb0-c5263c616426)

Further down in the script, we see a base64 string so let's decode it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4ceb0340-1cae-4a01-b73c-ee819887865a)

Now that we have the first and second part of the flag, we put it together and submit it:  
`HTB{w1ll_y0u_St4nd_y0uR_Gr0uNd!!}`

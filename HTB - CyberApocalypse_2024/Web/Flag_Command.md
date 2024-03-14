# Flag Command

## Enumeration

The web application provided starts as an old school game with prompts and we have to choose from some options:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2c9804e7-e3cf-407a-adad-a273d5f711d1)

We see it making a GET request to an API for some options:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/14206fcf-7bf2-445b-8d97-1c96c1942ab8)

Which shows us the possible commands:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6dc4f8c1-6488-4d31-9e29-f582d70c6c52)

## Solution
At the bottom we see a secret command. I wonder what that does if we input that instead of the expected commands:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12153139-6cd1-4781-b354-9d3a6e9f6bc3)

Nice, we got the flag:  
`HTB{D3v3l0p3r_t00l5_4r3_b35t_wh4t_y0u_Th1nk??!}`

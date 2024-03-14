# TimeKORP

## Enumeration

The web application gives us the option to check what time it is, or what date it is:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f0724e61-d804-486b-afb7-9025de74b838)

However, from the source code, we can see that it's executing the `date` linux command and using our user input, the `format`, without being sanitized.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6327ad50-c655-455d-8c05-e7192b921d70)

From the Docker file, we can also see where the flag should be:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/238fbd97-e8c1-4ace-8c01-a527083f051f)

In this case, we simply need to close the single quote for the date command, add a semicolon, our command, add another semicolon and use another single quote for the stderr redirect.

## Solution
Payload: `';cat /flag;'`  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fb2df9b0-0406-4d7d-8c7c-aeb2d1906ae1)

Nice, we got the flag:  
`HTB{t1m3_f0r_th3_ult1m4t3_pwn4g3}`

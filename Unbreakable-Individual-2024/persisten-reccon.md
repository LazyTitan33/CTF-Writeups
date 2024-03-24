# persistent-reccon

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/98e09b8e-80c3-485f-8d50-f2e972f32820)

# Solution

With this challenge, we only get a generic looking login page:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/06428772-2255-4b87-9455-70662516456e)

However, this challenge had an `OSINT` tag associated with it so we screenshot the login and do a Google reverse image search:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c8b2c1f5-a6ca-4f1b-b876-a5b609bb870e)

The first result mentions a `Westermo` product, clicking on it we can see a Lynx series switch:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7f58ead7-8dab-45d4-a7df-063fd80edf1c)

We can google for the default credentials:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ac2ca6db-166b-43bb-9694-5de63cd95fa2)

`admin:westermo`

We try and use that and we get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4ed986d8-6cf8-4598-8de0-81d4e421b1d7)

`CTF{7e33e33a06c53d77330b9621a62fd4f1915e6e695f3188aba62c6800695ee30e}`

# An unusual Sighting

## Enumeration
For this challenge, we receive two files. A bash history and the sshd log file.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2ac285ab-0307-4f7a-a032-b4220b111b62)

## Solution
We start the challenge by connecting to the provided IP and port:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/003250e1-5f88-4ce1-bf1d-8d6a6a8af999)

This answer can be found by looking through the sshd log file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7c2fbb90-2dd0-4a0c-8931-705d3504a9ae)

Second question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/049fe2b0-0c55-46e5-b488-828442075571)

The answer to this can also be found in the sshd log file by looking for the first instances of `accepted password` and `starting session`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a9eb3b87-24c2-43aa-af5b-3d3af9da1cb1)

Third question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4510300c-8a58-41ff-8583-81847f882d83)

I was puzzled by this one for a minute because nothing was defining what "unusual" means. But after looking carefully at the sshd log, I noticed a pattern in the login hours. Of course, it made sense, most of them were between normal business working hours, except one which was at 4AM:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1c284b63-a138-4d0c-bc62-472cb61e1741)

I initially missed it because I used to work OnCall as a systems admin so weird hours for login wasn't that weird to me. Moving on.

Fourth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8b20d63f-130f-4daf-8193-305af1695e6e)  
This can be found in the screenshot for the third question.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/afd2eb81-f624-4995-8431-7873312851f4)

Fifth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/59b7bf23-14a8-4d35-8db3-6f6c72a57ab4)  
Now we need to move our attention to the bash history. Since we already know the time when the intruder first logged in, we can easily tell the answer is "whoami".. plus, it's a classic ;)  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5066b374-c3c0-4535-aeb1-4130d0e471ba)

Last question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9523e244-84c6-4dad-8d3e-fd7501e3e844)

We can find the answer within the same log file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3d0e03d2-c0c5-4938-87f3-0ac6bc0e6db8)

`HTB{B3sT_0f_luck_1n_th3_Fr4y!!}`

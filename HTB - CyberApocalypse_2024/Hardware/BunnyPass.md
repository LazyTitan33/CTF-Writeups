# BunnyPass

## Solution 

As the description mentions, we are given access to a RabbitMQ instance with default credentials:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f5e2f810-cbfe-4063-94ab-afd246424236)

As it can easily be found on the internet, the default creds for RabbitMQ are `guest:guest` and `admin:admin`. Both work in this instance but give the same level of access.

This takes a bit of enumeration, figuring out the interface if you are not familiar with it, and eventually we get the flag in one of the messages from the Queues.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/05dbb095-8ccd-4330-904e-2b0917173cf1)

From the `factory_idle` queue, you can read the 6th message and get the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3ac57d48-013c-4e2a-bfa5-d36446bfea2a)

`HTB{th3_hunt3d_b3c0m3s_th3_hunt3r}`

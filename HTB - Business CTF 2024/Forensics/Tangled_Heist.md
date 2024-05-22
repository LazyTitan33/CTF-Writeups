### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/319e1019-8f9e-4702-9a08-f3b14cae756d)

## Solution

For this challenge we get a wireshark capture that we have to sift through and answer questions. In this situation, the wireshark capture contains LDAP traffic.  

#### Question 1:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/47c59fa0-4de0-4e4c-a193-e31ba9132b13)

Since LDAPS wasn't used, the traffic is in plaintext and we can see a first LDAP bind request on packet 10 by user `copper`:   
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/510cd7b9-ae31-4c8f-8875-9a9ed93ad658)

I lost many hours and even opened a ticket to support for this one because for the longest time, I was typing `cooper`. Don't be like me, take plenty of breaks and don't neglect sleep.

#### Question 2:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a160a0d9-aa47-42db-8af9-3e6a3347249c)

We can use the search for strings in Wireshark for this one and simply search for `Domain Controllers`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e3a6ebd3-9120-4771-8f83-faaba2201273)

#### Question 3:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7fb1db16-0b8f-4ae4-955c-4849fa49c2cb)

We know the answer for this one from the Distinguished Name.

#### Question 4:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/38428df0-51ee-42d7-bc70-43f4bc778a8f)

Again, we can use the search function to find Ranger and then have a look at the [badPwdCount](https://learn.microsoft.com/en-us/windows/win32/adschema/a-badpwdcount) value to get the answer.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2ebc4491-2de8-41cf-8854-ddfcc337e191)
#### Question 5:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/da60f692-9f9f-4c28-ba61-ef822a05263a)

Going through the wireshark capture, we can easily see the list of groups. We look for the `searchRequest` packet right before it and then look at the `Filter` value:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/45477d18-1879-4c6c-8dae-c259b66b25be)

#### Question 6:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fb1b0bda-87a6-4929-aeeb-b1f029fb8782)

The non-standard groups are at the end of the list of standard groups so we just count them:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2f684ff9-72fe-4d68-bd40-53fb90ea564a)

#### Question 7:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/08e3acaa-3064-438d-b27e-e0a355517779)

Doing a bit of quick research to refresh our memory, we know that disabled users will show up in LDAP with the `UserAccountControl` attribute set to `514`:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f83d1cfe-7478-4269-b3ec-f4adcb2883ac)

Going through the users, we find that `radiation` is the only user with 514.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7ab74c5b-f855-40dd-bf39-e867d54e26d4)

#### Question 8:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e51dde8d-d93a-4a21-9aac-9f3225e5084a)

Towards the end, after the attacker did his enumeration, we can see, in packet 669, the modification he made.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/33212e18-aaab-4ea6-b954-1ec9e04a5cef)

#### Question 9:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/94cc0a51-46d7-45cf-8257-1241eedb0a89)

In the same 669 packet, we can also see what the modification was:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3150424d-008d-4590-86c6-36b1dc38ab41)

#### Question 10:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ca839d10-3df6-4e06-973f-eccf05fdcb85)

In packet 671 we can see another user which is not following the same naming convention as the other ones so we can safely assume this is the user created for persistence.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8028acdd-e73f-48d6-9faa-c8df62c50bc2)

In packet 675 we can also see the group this user is in:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f8e53ec-8c01-4837-9754-d361571815e4)
#### Question 11:
Lastly, but weirdly this was the first step I actually did. I loaded the capture into [NetworkMiner](https://www.netresec.com/?page=NetworkMiner) and saw the asreproasted hash:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a7b9c5ca-9772-4810-8cdf-ab4399246074)

Passed it to hashcat and it quickly cracked it:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3612163c-1849-441b-afcb-3ffc66f67811)

And we have the final answer and our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b2e5b416-ee43-4a65-bd50-a1e3c34ad1ef)

`HTB{1nf0rm4t10n_g4th3r3d_2ff9f09034376d273b889164b91dbf15}`

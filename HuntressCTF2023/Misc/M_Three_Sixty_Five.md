# M Three Sixty Five

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/85103d8b-d0df-461b-8361-bf27dc566e8a)

### Solution
We first follow the instructions in the description and SSH into the box:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ef736b3a-35dc-4fef-a4e1-7bf4241fe56e)

Before anything, we do a little recon because we are curios. We list the running processes. In the screenshot below, you can see that I first redirected the output to a file and then read the file. This was easier for me to be able to read the entire content that was flowing outside the screen since we didn't have access to the less command which I would normally use.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e3401ec7-e5a4-46dc-93a2-b0a18c3251f4)

We found some credentials so we put that aside for now:

```
user: HackMe@4rhdc6.onmicrosoft.com
pass: HackHuntWin!
```
For the rest of the enumeration I used the AADInternals documentation to figure out what commands I can run:
https://aadinternals.com/aadinternals/#read-aadintconfiguration

#### 1st Flag:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6fd9cc13-5c2f-43dc-9374-1a4786f7dcfe)

```bash
Get-AADIntTenantDetails |grep street
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f3d66df2-fc25-4d86-b75a-5b3dd885d573)

flag{dd7bf230fde8d4836917806aff6a6b27}

#### 2nd Flag: 
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3a30b185-1179-4380-b27d-0024c09195f1)

```bash
Get-AADIntConditionalAccessPolicies |grep flag
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f39d1c5c-7d5e-4c5b-a051-a652cba4bcab)

flag{d02fd5f79caa273ea535a526562fd5f7}

#### 3rd Flag:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/59d18c6e-09b2-4b95-9c8e-0cb2efa3019f)

```bash
Get-AADIntTeamsMessages | Format-Table id,content,deletiontime,*type*,DisplayName
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5b7851a0-67b3-4fb7-bf0b-b610e6a70533)

flag{f17cf5c1e2e94ddb62b98af0fbbd46e1}

#### 4th Flag:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3954c5d8-db58-4db7-a499-063ba05d2f44)

```bash
Get-AAIntUsers |grep flag
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d6487958-e1ff-45ef-8197-aa25e293d777)

flag{1e674f0dd1434f2bb3fe5d645b0f9cc3}


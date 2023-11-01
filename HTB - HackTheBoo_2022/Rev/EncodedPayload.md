Nothing too fancy here. Running this binary with `strace`, we can see the flag is leaked right away. 

![image](https://user-images.githubusercontent.com/80063008/198257584-8df9b566-b00d-4003-868a-3ee2f0666ba1.png)

Generally running pwn/rev binaries with ltrace and strace are some of the first things I do in CTFs. It can leak a lot of good information.

HTB{PLz_strace_M333}
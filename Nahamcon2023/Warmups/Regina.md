# Regina

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7efa60d2-8203-4a98-8741-af8f1910ee10)

I first tried SSH-ing with no profile but failed.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cde3494f-9006-455e-b132-54034e4cd26c)

However, a strange banner that I haven't seen before comes up mentioning REXX-Regina. The challenge description also makes a reference to Rex. After some googling around, it turns out it's a programming language. I have found an example code to run linux commands on the link below:

https://www.ibm.com/docs/en/zos/2.1.0?topic=eusc-run-shell-command-read-its-output-into-stem

I created a `list_files.rex` file first because I first wanted to run a simple `ls` command without any redirections. I saw that it worked so I read the flag using the code below:

```bash
/* rexx */
address syscall 'pipe p.'                    /* make a pipe           */
'cat flag.txt'                               /* cat the flag          */

address syscall 'close' p.2                  /* close output side     */
address mvs 'execio * diskr' p.1 '(stem s.'  /* read data in pipe     */
do i=1 to s.0                                /* process the data      */
   say s.i
end
```
As it can be seen in the picture below, I'm sending the output of the .rex file directly into the SSH pty to run the code and it spits out the flag. It's messy but it works.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/103042cb-59d4-4bcc-996c-1daf2c889ed6)

flag{2459b9ae7c704979948318cd2f47dfd6}

I was very happy to get `1st blood` on this challenge. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/247faea9-5c3c-4a1e-9a94-94bb545c8b0d)

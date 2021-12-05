![image](https://user-images.githubusercontent.com/80063008/144766039-75b1df19-52f7-42a4-a0ef-13ee9c068cb6.png)

```
mr_snowy: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=d6143c5f2214b3fe5c3569e23bd53666c7f7a366, not stripped
```
```bash
checksec mr_snowy
```
![image](https://user-images.githubusercontent.com/80063008/144766045-2aac3713-1bf3-4f1a-941f-b9a56055881f.png)

Running the file locally we get this:

![image](https://user-images.githubusercontent.com/80063008/144766047-64d2c2dc-7ee4-413c-bea4-b57221742e72.png)

After we choose investigate we can deactivate and we get a segmentation fault if we enter a lot of characters.

![image](https://user-images.githubusercontent.com/80063008/144766050-3ba28b25-7688-4463-a223-a5a2b277fd68.png)

In ghidra, I found the deactivate camera function which reads the flag but it is never called by the binary itself. So in this case, we need to do a ret2win type of attack.

![image](https://user-images.githubusercontent.com/80063008/144766058-c8b8d558-e0af-494f-b8a6-ada568c271ea.png)

We have segmentation fault in the investigate function.

![image](https://user-images.githubusercontent.com/80063008/144766062-d3e79283-4177-442c-b3db-cf4d79ab26a0.png)

Opened the binary using gdb-pwndbg.

![image](https://user-images.githubusercontent.com/80063008/144766083-0e95c5f5-06a3-44e5-8bf8-2a640af69b43.png)

We can do info functions and can see the deactivate_camera function that reads the flag according to ghidra. 
![image](https://user-images.githubusercontent.com/80063008/144766094-1527cdcc-e930-4831-8fb8-b02ee30914ec.png)

We can disassemble deactivate_camera and see the functions in it if we want.

I want to find out what the exact offset is so we can do cyclic 1000 and then copy the long string.
![image](https://user-images.githubusercontent.com/80063008/144766100-fcfef88d-7e38-4627-8f03-344e88c84447.png)

Run the program and paste the string where we can get a segmentation fault. In this case after the second question.
![image](https://user-images.githubusercontent.com/80063008/144766105-5c601f4a-2616-440f-98a4-b5e3346725ae.png)

We get a segmentation fault so we can take the first 4 characters.

![image](https://user-images.githubusercontent.com/80063008/144766108-9f6f6a99-5a94-4a47-a635-f3cfd26ba080.png)

And run cyclic -l saaa to get the exact offset which in this case is 72.

![image](https://user-images.githubusercontent.com/80063008/144766110-32b76cce-089e-4390-a7c8-5ec63ea0306e.png)

We can use python to print 72 A characters and 6 B characters to confirm we have our buffer overflow where it needs to be.

```bash
python3 -c 'print("A" * 72 + "B" * 6)'
```
![image](https://user-images.githubusercontent.com/80063008/144766116-8b59e638-d440-4f3b-a588-5980c238b9c6.png)

Run the binary again in gdb and then paste the string and we can confirm we have injected the RSP.

![image](https://user-images.githubusercontent.com/80063008/144766117-13b6a222-265b-4956-bf5f-aa1ad8d3995d.png)

I used this model from cryptocat in order to script the pwn. I strongly advise you subscribing to his channel. He puts out great content and explains things much better than me.

https://raw.githubusercontent.com/Crypto-Cat/CTF/main/HTB/pwn/ropme/ropme.py

Followed the instructions in this video:
https://youtu.be/niPj8jYahV0?t=932


My edits to the original script:

Adjusted the symbol for sendline after:

![image](https://user-images.githubusercontent.com/80063008/144766151-19ad1369-d2cf-4ca8-8e6c-4e3ed7b68a68.png)

Remove break main because I didn't need to break to the main function.

![image](https://user-images.githubusercontent.com/80063008/144766155-bccc5c30-3a10-4fb6-814e-fa6c2e440351.png)

Adjusted the binary name to load our binary file:

![image](https://user-images.githubusercontent.com/80063008/144766161-ff3ab289-89ee-41a0-9a00-65f90c3ef73d.png)

Set the offset that I found with gdb-pwndbg. I could've also just let it find it on its own.

![image](https://user-images.githubusercontent.com/80063008/144766163-a99785bd-104c-4f45-abc7-8602dd7a43fc.png)

Because I had to deal with the first question, I got it to receive until > and then send 1 to answer the first question and receive until the next >.
![image](https://user-images.githubusercontent.com/80063008/144766172-2b080074-72cf-4ccd-b5e0-64f780a3cd35.png)

Setup my payload. Changed from dictionary to list (removed the {}). asm('nop') is no operation instructions instead of using characters for padding. Then specified the function where we want to jump, where we want to return. In this case deactivate_camera. I could take the address from ghidra or gdb_pwndbg but this script loads in the binary itself so it will know the function names.
![image](https://user-images.githubusercontent.com/80063008/144766175-68da9caa-444c-4445-b69d-49cf54efdbdd.png)

Then send the payload:

![image](https://user-images.githubusercontent.com/80063008/144766181-54e22cf7-bfa7-4a7f-9319-7b0634b24efd.png)

Make sure to have interactive at the end because we need to see the flag after getting the error message.

![image](https://user-images.githubusercontent.com/80063008/144766182-96894bca-8d92-4144-9cd3-18f2fd42ce00.png)

Used the syntax below to run it on the remote machine:

```
python3 mrsnowy.py REMOTE 134.209.26.37 32368
```
![image](https://user-images.githubusercontent.com/80063008/144766187-26eba9c2-b5ad-4546-881e-8fb3df0bac9d.png)

HTB{n1c3_try_3lv35_but_n0t_g00d_3n0ugh} 


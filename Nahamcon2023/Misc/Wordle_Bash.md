# Wordle Bash

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b47bddad-66c9-4bd9-bba2-d371bb42d012)

As the challenge description informs us, we connect with SSH to the box and then check to see what permissions we have. It seems we can run a script as root.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e98e64b4-b2ba-493b-8d9e-89fbbb069bb1)

The script is basically Wordle but implemented in bash. We need to enter a date and it has to match with the one the script randomly chooses. Which is impossible so that's not the solution.

After carefully reading the script, I noticed that `date` is also run as root and it's taking user input.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bf668e06-374b-4e9b-b4a9-ebd935732717)

As we know, `date` is a [GTFObin](https://gtfobins.github.io/gtfobins/date/#sudo) that allows us to read files. At first we need to go through the motions of selecting a date:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fa433e02-9b3e-4f46-9178-0a27e53dca93)

However, when it asks us if it is correct, we need to say no:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/82147e06-485a-483d-a5f3-94f95440ef06)

This is where the user input comes in. After we say no, we can enter arbitrary content so we just pass the `-f` argument and the file we want to read. If we try to read the flag, we get this message:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1f03529c-874f-4eba-a4db-9e6159a607b6)

This means we were able to read the flag.txt however it doesn't actually contain the flag. We need to escalate our privileges to get code execution as root. A logical step is to see if there is an RSA private key:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8af39181-28a3-4517-9b50-80a198fe528f)

Confirm it:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/29e989ec-3679-45aa-b534-d98367a2a9e0)

And we get the key:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/39d7e805-041e-44a4-9a2d-f50d2cab3a5e)

We clean it up and use it to SSH as root, we find a binary that we can run and it gives us the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9f84f728-2f7e-4d15-bc86-27c39bf74b21)

flag{2b9576d1a7a631b8ce12595f80f3aba5}

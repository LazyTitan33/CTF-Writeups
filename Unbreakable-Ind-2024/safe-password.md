# safe-password

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ca66ad51-b447-4700-aa7f-693c8909d6bb)

# Solution

This one gives us a leaked.txt file containing 150 passwords:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a361fea1-7872-4599-8ae5-46e86f1be329)

I couldn't think of an easier way so I manually started looking up passwords from this list in the [Have I Been Pwned](https://haveibeenpwned.com/Passwords) password database. I started with the lower half which seems to contain easier to write passwords:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b54ace86-c5da-48b1-bed4-d24f9f6090e5)

As per the challenge description, we are looking for a password that has been leaked at least 80 times before. We find that to be `Bubblegum123!`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/87164b5a-f2ae-4c17-a497-d1436cd96005)

And we have our flag: `CTF{fdc852bc63a266c8c38db64bef90d62d53ddeef00aa85df7b941ac780b3d75d8}`

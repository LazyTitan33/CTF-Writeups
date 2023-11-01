# Stickers

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5abfa008-e417-4a0b-a4e3-a66379f12120)

We have a simple sticker shop with some fields we can fill out:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/095f1407-93a9-49bd-9240-f6bfe3b88c28)

I tried this challenge early on and it was broken, it was supposed to generate a PDF but didn't. I struggled for a while then left it alone.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/276c4eba-5eb9-43b5-97b6-5b156a514cd7)

But I knew based on the error message that this was a DOMPDF RCE exploit:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/91933c66-3a4d-46a1-a7b2-b459ad0944ab)

Luckily at some point I saw this message in the Discord channel.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3ea3ad27-ad0c-4ea9-9f8f-22a2749db863)

Good thing I started searching for other people talking about Stickers otherwise I wouldn't have seen this and probably wouldn't have gone back to the challenge. Perhaps a better idea is to also leave such a note in the challenge description or pinned to the discord channel.

We can see that now PDFs are generated:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/04f383e4-12d9-43a4-8531-4193e8a52ae0)

DOMPDF has a known RCE vulnerability detailed [here](https://github.com/positive-security/dompdf-rce) and [here](https://positive.security/blog/dompdf-rce). I used a stylesheet href.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7561b844-08f6-4bee-acc1-28a8bf20f8cc)

And indeed we get a hit on our python webserver for the files we prepared.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/63bec8b6-79b9-4f5a-b8e5-b4e0761b73f3)

We can easily find the path of the dompdf fonts due to the Forbidden error message:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7bc7c485-f19b-4c0e-b88c-9c836383ff12)

The `.css` file we prepare will grab our php webshell:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/36d1075a-1ab3-4065-91df-fe3d749b0ab7)

We can get the md5um of our path because we'll need it to find our webshell:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/774e6e2b-a219-42e4-94aa-21caeb956466)

The webshell is inserted into a renamed font file:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/691f2b3a-80b1-43a2-8a1f-18dfe28fc7c3)

And we have our code execution and our flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/616a12af-72fb-4bf2-a2bd-5d556f3aaa0e)

flag{a4d52beabcfdeb6ba79fc08709bb5508}


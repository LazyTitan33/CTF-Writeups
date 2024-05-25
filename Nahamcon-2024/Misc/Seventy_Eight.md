## Seventy Eight

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/443b70bb-b943-4a68-b0dc-6dee30abcf1a)

## Enumeration

This was a very interesting challenge. It is expecting some input from us:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/60ba4d29-8ac9-4951-ba2d-6ea041c5a594)

I played around with that for a while but then I started researching. I realised that this was all about esoteric programming languages and [this](https://github.com/angrykoala/awesome-esolangs) is a good repo with examples of such languages.

One of them is actually called [78](https://github.com/oatmealine/78).

I won't try to explain how it works here. Even after reading it a bunch of times, it was still very tricky to get the right syntax. I strongly recommend taking a hands on approach here as that is the best way to learn.  

## Solution

After some experimenting and gathering the required letters, I managed to get to this point where I could get it just right:  

```text
aaaaaaaaaaaaaaayrb
aaaaabababayrb
aaaaaaaaaaaaaaaaaabababababababayrb
aaaaaaaaaaaaaaabyrb
aaaaaaaaaaaaaaaababayrb
aaaaaaaaaaaaaaaabbabaaayrb
aaaaabababayrb
aaaaaaaaaaaaaaaabbabayrb
aaaaaaaaaaaaaaaababababayrb
aaaaaaaaaaaaaaabyrb
aaaaaaaaaaaaaaaabbayrb
aaaaabababayrb
aaaaaaaaaaaaaaaayrb
aaaaaaaaaaaaaaaababababayrb
aaaaaaaaaaaaaaababababayrb
aaaaaaaaaaaaaaabyrb
aaaaaaaaaaaaaaaaaaabbbbaayrb
aaaaaaaaaaaaaaababababayrb
fuck!
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2b35c16f-d834-4626-8472-829f79bd00f8)

`flag{7deea6641b672696de44e60611a8a429}`

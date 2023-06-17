# Glasses

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/30535159-715f-4628-8251-7cfbc94fb022)

When checking the source code of this web application, I noticed a large blob in the HTTP response in BurpSuite:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/02c0e735-6415-49e6-8b89-70df0069379b)

Scrolling all the way down, we can see it's actually javascript. I tried multiple ways to run it, in the browser console, beautifying it and running it in online parsers but the output was too large and I couldn't get all of it.

So I resorted to saving it locally in a file and changing it a bit to print the code:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0431ba0a-a95a-478f-abd8-2c29a654f0a5)

Then I used node to run the javascript and redirect the output to a file. Again, there was a lot of content (garbage) but doing a simple CTRL+F helps us find the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6aba3aaf-8460-471a-a26e-53c0ec18162f)

flag{8084e4530cf649814456f2a291eb81e9}

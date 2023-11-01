# Layered Security

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/493eb329-1441-4611-9594-77454df58982)

### Solution
As usual, we start by running the file command on the provided file and we see it's a GIMP file:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e53c67dd-9a0f-4eef-9acc-aaa32943f77e)

I searched online for ways to open this without installing GIMP:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c75b3178-d615-49d1-9ae2-f1f2400ef730)

The first result in DuckDuckGo was very helpful. I don't recommend searching for these kinds of tools using Google as you get a lot of ads and shady websites.
https://fixthephoto.com/online-gimp-editor.html

Uploading the file in this tool, we can see a bunch of pictures in various layers, thus the name of the challenge. Even in the thumbnail, you can see that Layer #3 isn't just a picture:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e460fa42-3be3-4363-ac1f-d3dc382ca362)

In fact, if we click on the small eye icon for the top pictures to hide them, we get to this layer and get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ff2db2da-33ca-428e-a41a-edfd94e23cb2)

flag{9a64bc4a390cb0ce31452820ee562c3f}

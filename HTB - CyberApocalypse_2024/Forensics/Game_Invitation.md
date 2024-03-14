# Game Invitation

## Static Analysis
For this challenge, we receive a Macro enabled word document as denoted by the extension `.docm`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/82231574-a8ca-4397-9c9b-a5b0c9cd15d5)

When dealing with such files, first we can use `olevba` to see what macros they might be hiding. 

```bash
pip install oletools
olevba invitation.docm
```

This gives is an obfuscated VBScript.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/69b57251-952d-4482-8212-951c3f7181d0)

From this part of the code we can tell that at a certain point it `deletes a js script`. It also will autoopen only if the USERDOMAIN variable of the windows machine is `GAMEMASTERS.local`. Let's look further into the code.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/91562e8d-e015-420a-bc92-6d567eea5524)

In this code, we can see that it creates a file then puts it into `appdata\roaming\Microsoft\Windows` and calls it `mailform.js`. This is the js file it is supposed to delete. More code below:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e66735ae-1886-4c35-ad9d-6306a5b7c75f)

The last part of the code runs the script with the `vF8rdgMHKBrvCoCp0ulm` string as an argument. We'll save this for later.  
We could try to decrypt the xored and obfuscated script but I find it easier to do dynamic analysis now that we know more about what we are dealing with.

## Dynamic Analysis
In a segregated VM I just YOLO it (carefully try not to detonate anything) and open the file to look at the macros. In this case it's safe because it checks the USERDOMAIN variable and because it doesn't match the target, it doesn't do anything.

Before we actual allow it to create the mailform.js file, let's change the default apps by file type from Windows so that it won't actually run the script. Instead I change it to open it in Sublime text.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e27b128d-7d25-4c53-bb5e-6b1cf5649cf7)

Now I change the `GAMEMASTER.local` from the macro to my VMs USERDOMAIN and open the file. As soon as it does, it opens the mailform.js file in Sublime and we get the next stage of the "invitation".  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bfae10d3-f33a-49ab-955e-1379f533dcc6)

A very good and helpful tool we can use for deobfuscation here is [de4js](https://lelinhtinh.github.io/de4js/). Slap that badboy in there we see a function with a variable that has a large base64 blob.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/58aa951e-f6dc-49ca-b934-4a8bbd5f829c)

There are a couple other function with random names. I give that code to ChatGPT to explain what it does and it turns out it's just an RC4 encryption written out. This reminds me of the string that's passed to the script at the end. That must be the key to decrypt the file when running it.

So I just take the Base64 blob, put it in Cyberchef, decode it and use the RC4 recipe with the passphrase to decrypt it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4e2743e5-fb92-4fc6-a63e-025c9a58491c)

We get another stage of obfuscated javascript code that we take care of using [de4js](https://lelinhtinh.github.io/de4js/) and while scrolling through it, we see our flag set as a cookie:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6ac5cd3d-a29e-446b-9e35-ac9164fa113f)

Decode it and get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/764e2a83-f0f5-495f-b26a-d0ed20e904d1)

`HTB{m4ld0cs_4r3_g3tt1ng_Tr1cki13r}`

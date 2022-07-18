In this challenge we get only one file with an extension I wasn't familiar with.

![image](https://user-images.githubusercontent.com/80063008/179479263-ec322764-6b22-461d-9e14-e1fc17789378.png)

After some googling around, we find these are Chrome browers extensions. I don't remember the challenge description but I think it might've mentioned it as well.

We can unzip this file and get what is inside.

![image](https://user-images.githubusercontent.com/80063008/179479464-50dc8215-eaae-436d-9205-4cf52ca212e0.png)

In background.js we see a long obfuscated javascript string.

![image](https://user-images.githubusercontent.com/80063008/179479517-ac1a6825-640a-466d-8dc4-895e6fc251b3.png)

I went to https://deobfuscate.io/, pasted it there and got something more readable.

![image](https://user-images.githubusercontent.com/80063008/179479555-70425145-fc02-45fa-928a-e78e96ba7230.png)

Putting that in Sublime and enabling wordwrap, we can see yet another layer of obfuscation.

![image](https://user-images.githubusercontent.com/80063008/179479688-f909d29e-143d-4d72-b56d-fcafd437b76d.png)

It is defining a variable called q which has an array of strings. Most are empty, others contain text. I didn't know of an easier way to do this so I'm looking forward to see other people's writeups. What I did was a lot of manual deobfuscation.

I pasted the entire q variable into the console of my web browser. Then took each length of q values that were concatenated and pasted them to get the output. Here is an example.

![image](https://user-images.githubusercontent.com/80063008/179480065-00f353b2-0e4b-466c-8bdf-2d853e7e2788.png)

Slowly, I replaced all of them to get something more readble.

![image](https://user-images.githubusercontent.com/80063008/179480121-b713250e-c1ca-4d34-aeda-400f421e2005.png)

Altough not properly formated for a valid javascript code, I could still read and get an idea of what was happening. 

In short, we have what looks like a HEX strings that is AES-CBC encrypted with the `_NOT_THE_SECRET_` value which is acting as both the Key and the IV. Putting that into Cyberchef we get the flag.

![image](https://user-images.githubusercontent.com/80063008/179480472-3ca0cff1-88d6-4b7c-94be-79ac6177952f.png)

HTB{__mY_vRy_owN_CHR0me_M1N3R__}

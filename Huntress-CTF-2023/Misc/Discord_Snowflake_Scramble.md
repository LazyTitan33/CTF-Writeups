# Discord Snowflake Scramble

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3b60266a-9def-4f1e-ae18-36b7939da712)

### Solution
This one required some googling but because of SEO, a lot of results were nothing I was interested in so I switch search engines and used duckduckgo:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ee9e5f69-d826-44d7-a0fc-2ca05e9c85d3)

The first 3 results show tools that parse the IDs in the link we were provided differently. Turns out these IDs are called Snowflakes and they can represent either a Message ID, or a Server ID, a channel ID etc. The tool that ultimately helped me further was [discordtools](https://discordtools.io). I was reticent at first because for it to give you detailed information, other than the timestamp of the snowflake, they require you to login with your Discord account. However, the good news is that it's an Open Source application with their code on Github so that was reassuring for me.

I inputted the first Snowflake from the link and sure enough, getting the detailed Discord info, we can see an Invite link:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/93bf427c-8a5e-426c-ac89-fe7c35e1ff56)

Accessing that link gets us on this hidden server and we have the flag in the channel with the same name:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/11fece46-a83e-4722-8098-8580d07a73a3)

flag{bb1dcf163212c54317daa7d1d5d0ce35}

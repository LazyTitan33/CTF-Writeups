# Rogue Inbox

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9a728756-93f4-4597-9a04-51fbcb1a90fe)

### Solution

We get a .csv file with lots of data in it. We can open it in Excel and filter based on UserId because we already know from the challenge description that Debra was compromised. Taking a long time to look through this data, I was trying to see if I can spot any anomalies. Then it hit me... there were a lot of `New-InboxRule` set up which is out of the ordinary. People do set up inbox rules but rarely that many in a quick succession so I applied a filter to show only the New-InboxRules as well and focused on these.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2f5d33c4-d6b3-423c-b73a-6fb5549c342b)

Then I saw it.. a letter peaking out at me:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/010eca45-de68-4665-98e7-e6807cb1c0c6)

Then I saw another one:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2de97f89-9305-4b6f-ad2c-86dfdc71a4ac)

And another:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a0d4282a-bfd8-4a90-905e-9052b791d4ce)

You see where I'm going with this:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7c4d4e35-f567-4ca8-8a26-c792e8e72036)

Let's use some bash onliner magic to carve this out:  

```bash
cat purview.csv|awk -F "520c2525d932" '{print $2}'|awk -F '"' '{print $1}' ORS=|sed 's/\\//g'
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/61d56fa0-d9be-45e7-8328-dcf1e211a8b2)

flag{24c4230fa7d50eef392b2c850f74b0f6}

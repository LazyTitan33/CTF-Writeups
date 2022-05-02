This was the OSINT series of challenges. I was not able to go through all of them but unlike other OSINT challenges from other CTFs this one was much more fun. It was focused and had a storyline to it so it didn't feel like you were just scavenging for info on the internet.

<h1>1st Challenge:</h1>

![image](https://user-images.githubusercontent.com/80063008/166226011-fb7226ca-fe12-4d6a-afdd-01b5864320c8.png)

It starts off pretty easy. We can google the name of the company: 

![image](https://user-images.githubusercontent.com/80063008/166226066-eb42de84-0e85-45f8-9da4-1c7e21b23dcd.png)

We find their website and input it into [who.is](https://who.is/whois/keebersecuritygroup.com) and get our 1st flag.

![image](https://user-images.githubusercontent.com/80063008/166226135-909b1cef-4c1b-40aa-b94f-3f3480335e16.png)

<h1>2nd Challenge:</h1>

![image](https://user-images.githubusercontent.com/80063008/166226240-cb5d247b-12eb-45bd-ae25-dc90e97311bb.png)

On the company [website](https://keebersecuritygroup.com/team/) we can see their current team. If we want to see what changed on this page, we go to the [Wayback Machine](https://web.archive.org/web/20220419212259/https://keebersecuritygroup.com/team) and find our 2nd flag.

![image](https://user-images.githubusercontent.com/80063008/166226248-56277f75-6758-4d6a-b363-736e71107b1a.png)

<h1>3rd Challenge: INCOMPLETE</h1>

![image](https://user-images.githubusercontent.com/80063008/166226576-98ee77f5-c34f-4041-89bc-ed3ed2e74f65.png)

Now that we know the name of the ex-employee, we can search for her on [github](https://github.com/keeber-tiffany) and find that she had two commits in two different repos.

![image](https://user-images.githubusercontent.com/80063008/166226775-21acb06f-7587-4cd9-b290-8d5196a8314b.png)

Let's take the first one using:  
`git clone https://github.com/keebersecuritygroup/security-evaluation-workflow`

We can see the history of the commits using:  
`git log`

One of the commits looks particularily interesting considering the description:
![image](https://user-images.githubusercontent.com/80063008/166226902-2f739537-3e0b-4a17-8f97-b15abe38004f.png)

We can see what was commited using:  
`git show 3115bda63937831d2b43d52bbebe6b352ccedc30`

![image](https://user-images.githubusercontent.com/80063008/166226952-f37b40dc-8e0b-4292-8b95-54ba251beb7e.png)

From here, I ran out of time. I tried researching Asana and their github integration but I ended up on rabbit whole reading the wrong documentation. There are other writeups available which explain that there was an Asana API that could've been used with this secret.

<h1>5th Challenge:</h1>

![image](https://user-images.githubusercontent.com/80063008/166227167-56c4e20f-0d1b-4056-9a5a-834b0260128b.png)

I found this by chance while I was curiously reading all the commits from this repo.

![image](https://user-images.githubusercontent.com/80063008/166227204-640127c5-3071-438b-b1c6-aeab4ba21d35.png)

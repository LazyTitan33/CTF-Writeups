### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/862019ba-68da-4d94-8246-500175943317)

## Enumeration

This challenge gives us a `database.rs` file, a `source.rs` file and a `.git` repo:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a9e0ca6c-b8fe-4ae6-90a1-414bc3ce9f3c)

Nothing interesting was visible in the two rust file, but we can start enumerating the repo by checking the log first:

```bash
git log --all --graph --decorate
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ee87e14f-31b5-4b3e-9324-11e272d07a16)

We can see a `main` branch and a `w4rri0r-changes` branch. Doing a `git show` on the commit from the `w4rri0r-changes`, we find the first part of the flag.

```bash
git show bfa416eaeaff63de8f5118be829f669ffd0cc6a7
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/49801792-bfa2-4a31-a8ed-d200293c1ce5)

We can see in the second commit that they removed some sensitive information:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5b8ed44b-99fe-4aea-becd-6b7732d47b95)

```bash
git show 1501091a639e565d40a2b3b20df3227e86d72a0e
```

Specifically, they changed the `database.rs` file:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/79a18c98-ef29-4dbd-a817-1fceea3516f2)

So in this case, if we want to have a look at the database.rs as it was before removing the sensitive content, we can use `git checkout` one commit prior. In this case, the initial commit.

```bash
git checkout ae4f456dcfe1e989ce13ca25231ac5df2fc4380d
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f0212ffb-a02e-40c0-b872-fcc5d77fc966)

Now we load the datatabase in sqlite3 and get the second part of the flag.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ee7e95cd-304f-4d25-85f1-b634f69ba689)

And lastly, we can do a git show on the latest commit which seems to be just a stash, and we get the 3rd part of the flag:

```bash
git show a38932590c3265c1c2e0160a70e449ecfb39d3e2
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6d5fe731-062e-47bf-ab44-850df04dfb19)

## Solution

Putting it all together and we have our final flag:  

`HTB{g0t_tH3_p4s5_gOT_thE_DB_g0T_TH3_sT4sH}`

# Land Before Time

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/21e6fbd9-94f1-4810-ace4-c9d10bef0551)

### Solution
The challenge description indicates the tool we should be using: `iSteg`. A quick google search helps us find it:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/38766877-410b-4c69-85a2-5f540deb1f19)

We can find a pre-compiled binary here:
https://github.com/rafiibrahim8/iSteg/releases

Being a java application, we can open it using the syntax below:

```bash
java -jar iSteg-v2.1_GUI.jar
```

Once we open our provided png file, we get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/36521aa0-786c-4658-9e7b-6d333b832282)

flag{da1e2bf9951c9eb1c33b1d2008064fee}

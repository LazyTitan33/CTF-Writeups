In this challenge we get a docker and, in the Dockerfile, we can see that an rbash shell is created for the user.

![image](https://user-images.githubusercontent.com/80063008/227537610-78c05960-ea45-42d2-9d19-588d39c84314.png)

We can bypass this when we SSH into the machine using `-t 'bash -noprofile'`

```bash
ssh restricted@134.122.102.219 -p 31219 -t 'bash -noprofile'
```

This allows us to no longer be restricted and exit our home directory and read the flag:

![image](https://user-images.githubusercontent.com/80063008/227537791-cafce5e9-5b5a-4668-94b3-f4f7c0e234bd.png)

HTB{r35tr1ct10n5_4r3_p0w3r1355}
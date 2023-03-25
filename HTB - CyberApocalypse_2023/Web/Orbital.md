I saw another login screen for this challenge:

![image](https://user-images.githubusercontent.com/80063008/227707125-470c5d41-3140-40a3-812e-84cf93f9a20c.png)

I was also trying to do other things at the same time so I didn't pay it to much mind. I saved the first login request I tried, put an asterisk in the username field to tell `SQLMap` where to inject and started it with the syntax below:

![image](https://user-images.githubusercontent.com/80063008/227707417-b8c0e32f-32b0-4036-aa61-07d9d2b2a776.png)

```bash
sqlmap -r req.txt --batch --dbms=MySQL --dump --ignore-code 401
```

-r = Load HTTP request from a file  
--batch = Never ask for user input, use the default behavior  
--dbms=MySQL = tell SQLMap what type of DB where working with, we know it from the source code  
--dump = Dump DBMS database table entries  
--ignore-code 401 = for some reason SQLMap kept throwing this error so I told it to ignore it  


After a short while, it found two types of SQL injection:

![image](https://user-images.githubusercontent.com/80063008/227707407-c4ca656c-1132-46df-82b2-0575de423047.png)

And it even was able to crack the admin password by itself:

![image](https://user-images.githubusercontent.com/80063008/227707434-c3513c6d-b970-4e79-8d5f-57b86280f038.png)

1692b753c031f2905b89e7258dbc49bb (ichliebedich) 

After we logging in as the admin we see the main page:

![image](https://user-images.githubusercontent.com/80063008/227707455-1cb9979d-fec1-4cf9-b69c-c03bc5b6c56f.png)

Further down we see an `export` function:

![image](https://user-images.githubusercontent.com/80063008/227707477-b376e118-c190-49f0-acbe-9a0f107838d9.png)

Testing to see how it looks and what it does, we see this request in BurpSuite:

![image](https://user-images.githubusercontent.com/80063008/227707506-fe5f018c-f689-4c39-9eea-99b711f5fa25.png)

Based on the source code, in the `Dockerfile` we can see that the flag is copied in the root directory and name `signal_sleuth_firmware`:

![image](https://user-images.githubusercontent.com/80063008/227707562-2b796d0e-3a08-4fee-9d06-d6a9dc043e04.png)

In the `routes.py` source code we can see the export function which seems vulnerable to LFI via `../`

![image](https://user-images.githubusercontent.com/80063008/227707591-a609c771-28f4-4355-a2c2-a5833e640682.png)

We try it and easily get the flag:

![image](https://user-images.githubusercontent.com/80063008/227707612-3e5c5542-1c4a-4405-beb8-6a0c59568b3e.png)

HTB{T1m3_b4$3d_$ql1_4r3_fun!!!}
![image](https://user-images.githubusercontent.com/80063008/166223338-fe251823-f500-44b5-a98b-435158b68c60.png)

When connecting to the challenge we see we have some options.

![image](https://user-images.githubusercontent.com/80063008/166223379-514c8bf6-5482-40ee-bba2-ccde34d7dff0.png)

Choosing option 0 gives us a tutorial on RSA cryptography. Choosing option 1 starts the quiz. We first get a short n, e and ct.

![image](https://user-images.githubusercontent.com/80063008/166223479-bb50e097-14e3-4d79-a19b-f59dbe25e1af.png)

We can pass those to [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) and it will do the work for us.

`./RsaCtfTool.py -n 124762191422189 -e 65537 --uncipher 64370744219044`

![image](https://user-images.githubusercontent.com/80063008/166223577-00d77f08-28c2-4d84-92fa-0726d925d364.png)

We need to provide the answer in Big Endian. Repeat this two more times and we get the flag.

![image](https://user-images.githubusercontent.com/80063008/166223615-ac76ff60-cdea-4fba-9553-63a1927230a7.png)

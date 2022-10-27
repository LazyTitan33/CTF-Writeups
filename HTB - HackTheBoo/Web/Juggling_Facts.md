The title of this challenge gave the attack away immediately for me. As soon as I saw that the source code is PHP I knew this is a Type Juggling vulnerability.

We can see in the source code, specifically the entrypoint.sh file, that the flag is in secrets. 

![image](https://user-images.githubusercontent.com/80063008/198254556-ec45546c-61f1-4ba8-b074-9a8d7d637a8c.png)

We try to read that but get the error that it can only be accessed from the localhost.

![image](https://user-images.githubusercontent.com/80063008/198254660-b7e73e6c-304d-4ff6-9dee-9db71b16a8a7.png)

We switch the type to boolean `true` and we get the flag.

![image](https://user-images.githubusercontent.com/80063008/198254713-c0197a98-bd59-4045-83e7-8419ce52c3ae.png)

HTB{sw1tch_stat3m3nts_4r3_vuln3r4bl3!!!}

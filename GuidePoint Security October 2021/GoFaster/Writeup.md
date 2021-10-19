We are given a text file:

![image](https://user-images.githubusercontent.com/80063008/137870318-48f400e1-fe49-4057-b537-88048f1811a7.png)


With 19999 lines of hex codes:

![image](https://user-images.githubusercontent.com/80063008/137870332-a967a39c-6fde-4256-ae35-e4d51936f863.png)


Converted what I expected to see in a flag (CTF) to hex:

![image](https://user-images.githubusercontent.com/80063008/137870346-87fbeae3-65ff-462c-b7d1-e08b11e44a00.png)


Then grepped for that string in the entire file:

```bash
grep "435446" GOFASTER.txt
```

![image](https://user-images.githubusercontent.com/80063008/137870366-c3e81067-5520-48f1-8fd0-af4adf85eef2.png)


Based on the positioning of the string in the hex, I figured the second one should be the flag.

![image](https://user-images.githubusercontent.com/80063008/137870376-b9cdd507-8790-4ce9-a250-fbc683963e98.png)


StormCTF{Learners:Encoding4:56fe2c8aB2A2cA0EedaA54f499fcfd1a}

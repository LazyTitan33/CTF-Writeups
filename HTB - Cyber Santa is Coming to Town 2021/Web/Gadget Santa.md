![image](https://user-images.githubusercontent.com/80063008/144765128-e1ee76a8-eed0-4455-b6e4-5fa606e7c1dd.png)

The homepage shows us a monitor with a few options.
![image](https://user-images.githubusercontent.com/80063008/144765112-cc140c22-4ebb-4153-825f-04331c76f67c.png)

Clicking on them we can see they are commands being executed.
![image](https://user-images.githubusercontent.com/80063008/144765162-19be83f7-f559-43f6-88a8-45bb01219dc2.png)

The source code /config/santa_mon.sh shows us how these commands are executed.

![image](https://user-images.githubusercontent.com/80063008/144765511-3e55fdda-271f-4337-a690-9ead72bcb0e3.png)

If we try our own command, like ```id``` we can see it is executed.

![image](https://user-images.githubusercontent.com/80063008/144765307-a84c4d00-5134-42e6-8275-5a8e3791ec58.png)

However if we try a command that has a space like ```ls -la``` for example. We do not get an output.

![image](https://user-images.githubusercontent.com/80063008/144765319-97a99570-eb51-4cdc-97e7-e598cc504765.png)

Looking at the source code in /models/MonitorModel.php, we can see why. There's sanitization in place to replace the space with nothing thus making our commands invalid.

![image](https://user-images.githubusercontent.com/80063008/144765336-36100f4b-f0ed-4e63-aecd-9db15ef6f0ad.png)

A quick google to bypass bash space restrictions we can find multiple suggestions on hacktricks.

https://book.hacktricks.xyz/linux-unix/useful-linux-commands/bypass-bash-restrictions#bypass-forbidden-spaces

We know where to look for our flag thanks to the source code in /config/ups_manager.py

![image](https://user-images.githubusercontent.com/80063008/144765419-7c7fa49a-06a8-4a97-87c5-b7c20e3ecd72.png)

I tried with ${IFS} and it worked. I had to make sure to use the semicolon ```;``` bash operator to separate the command that it was expecting from the bash script and my own.

![image](https://user-images.githubusercontent.com/80063008/144765195-c33c3205-b4f9-442d-86a4-a9904111993f.png)

HTB{54nt4_i5_th3_r34l_r3d_t34m3r}

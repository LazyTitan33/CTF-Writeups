
![image](https://user-images.githubusercontent.com/80063008/144765958-176f1736-eec0-484f-a542-53430820f88f.png)

We get a file called client.
```
client: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=bcb9d17215725749cf2ce0ee9ef5df3c98ba8f00, for GNU/Linux 4.4.0, stripped
```
When running it locally would only connect back to the port I gave it and just write back to me whatever I typed but in reverse.
![image](https://user-images.githubusercontent.com/80063008/144765980-58b87af1-9f7c-42c5-8cbe-8d24bf65e417.png)

![image](https://user-images.githubusercontent.com/80063008/144765970-8656dc45-64d3-455a-91f8-7ea1de4e0d26.png)


When running it remotely I could only get.

![image](https://user-images.githubusercontent.com/80063008/144765974-ee1ea3e0-24be-4ba5-aca8-ca4fbfce2329.png)


Ran it with strace to see more of what it is doing and I got the flag.

![image](https://user-images.githubusercontent.com/80063008/144766006-a3260555-8570-4524-99d2-8383027e8fb6.png)


HTB{n0t_qu1t3_s0_0p4qu3}


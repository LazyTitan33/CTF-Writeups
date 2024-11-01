# Finders Fee

![image](https://github.com/user-attachments/assets/6e38ed81-b5f2-4752-823e-4e703b47efee)

## My Solution

We are dropped in a shell where the `find` command has SUID permissions and the flag is in the `finder` user home directory. Looking through the help section of the find command, we can see that using the `-files0-from` argument, it allows us to give it a file as an argument from which to read files.  

![image](https://github.com/user-attachments/assets/2dfc11cf-283b-4cce-ac58-a4deba4a9620)

However, similar to other binaries, when it is not finding the file you provide, it tells you with a verbose error message and as such you can leak information. 

```bash
find -files0-from /home/finder/flag.txt
```

![image](https://github.com/user-attachments/assets/e9dc2dac-da8c-4a22-9477-e887252f5ab6)

`flag{5da1de289823cfc200adf91d6536d914}`

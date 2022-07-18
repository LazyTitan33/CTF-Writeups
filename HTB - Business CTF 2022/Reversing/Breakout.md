On Breakout we are given an IP and port. Visiting it, we can see what looks like a Linux directory structure.

![image](https://user-images.githubusercontent.com/80063008/179477633-fc2b9180-bc16-45a8-896e-b136b6f31cc2.png)

The second one though is not a directory but a file. It can be noticed that it is missing the / at the end which denotes directories.

We can download that and running file on it, we see it's an ELF binary.

![image](https://user-images.githubusercontent.com/80063008/179477821-f1b18c33-504c-412d-9291-99207b6aaf54.png)

First thing I usually do is run strings on these. Grepping for HTB we get a part of the flag.

```bash
strings bkd|grep HTB
```

![image](https://user-images.githubusercontent.com/80063008/179477924-09fb0453-c005-41ba-81cc-b918cc2b92f2.png)

With grep, we can use the -A flag in order to show x amount of lines after the result. In this case I needed to see 8 lines to get the entire flag.

```bash
strings bkd|grep HTB -A8
```

![image](https://user-images.githubusercontent.com/80063008/179478895-c5b48062-2ae4-4b64-ab53-58d0540d1578.png)

We need to get rid of the H at the end of each line.

```bash
strings bkd|grep HTB -A8|sed 's/H$//g'
```
![image](https://user-images.githubusercontent.com/80063008/179479012-10c898ba-4a89-4d9a-9913-50c022ec2baf.png)

Now we need to remove the newlines and can use tr (transform) for that.

```bash
strings bkd|grep HTB -A8|sed 's/H$//g'|tr -d '\n'
```
![image](https://user-images.githubusercontent.com/80063008/179478652-222955c0-6eab-4511-aa3a-39016379d412.png)

HTB{th3_pr0c_f5_15_4_p53ud0_f1l35y5t3m_wh1ch_pr0v1d35_4n_1nt3rf4c3.....}

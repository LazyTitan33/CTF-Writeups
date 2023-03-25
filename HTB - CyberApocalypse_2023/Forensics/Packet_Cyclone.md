For Packet Cyclone, we receive a bunch of .evtx files, Event Viewer logs, to analyze, and some predefined sigma rules:

![image](https://user-images.githubusercontent.com/80063008/227505409-781f9a08-9c51-476c-8f28-f5fa4574ed9a.png)

The Challenge description seems to indicated to us that we should be using `chainsaw` and the sigma rules they provided.

![image](https://user-images.githubusercontent.com/80063008/227505574-a042ce77-56e9-47eb-9c45-264db30a3815.png)

I had a different approach. I used a tool called `evtx_dump.py`, which you can install with `sudo apt-get install python3-evtx`, to convert the .evtx files to their .xml equivalent. This allows me to easily read the content of each log in the linux terminal.

I used this quick bash line to do it for each file and output it in the converted folder.

```bash
for file in ./*.evtx;do evtx_dump.py "$file" > converted/"${file%.evtx}.xml";done
```

For this challenge, we had to answer the questions that we get from their docker instance in order to get the flag. The first question:

Question 1:  
![image](https://user-images.githubusercontent.com/80063008/227506179-ec233ae5-f8f7-4755-a184-1cc7c11882b2.png)

I got that answer by using `cat` to read all the .xml files and using grep with a regex to look for email addresses. I asked ChatGPT to give me this regex because I'm lazy. I also added the `-r` flag for recursive because this shows me the file where the match was found.

```bash
cat * |grep -rE '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
```
![image](https://user-images.githubusercontent.com/80063008/227507538-43230b22-a523-40bc-9c22-9813713b542c.png)

Question 2:  
![image](https://user-images.githubusercontent.com/80063008/227506577-4777ffcc-5652-4eb7-8314-9a0c8f40767f.png)

The answer to this was in the same line we got using the above grep.

Question 3:  
![image](https://user-images.githubusercontent.com/80063008/227506762-518efaa7-967f-4b28-b7f5-395ea6106d31.png)

Again, we got this answer from the same command as above. So with one grep, we got the answer to 3 questions. We just had to look at the [rclone documentation](https://rclone.org/commands/) a bit to understand the syntax and arguments and we can tell that after the remote argument, the cloud storage provider is entered. 

![image](https://user-images.githubusercontent.com/80063008/227507673-e594ed82-1b78-4e21-89e0-5cc1c2d5d1cf.png)

Question 4:  
![image](https://user-images.githubusercontent.com/80063008/227507746-597a7bee-408d-4fd7-bfa1-a42b7eea10ca.png)

To get the answer to this we can simply open the `Microsoft-Windows-Sysmon%4Operational.xml` file indicated by our grep and search for the password and we can see the ProcessId:

![image](https://user-images.githubusercontent.com/80063008/227507912-4995fe10-0068-4ece-9e0f-41683e7c6274.png)

Question 5:  
![image](https://user-images.githubusercontent.com/80063008/227508206-1704f411-6c02-443b-b588-a15e50311d8f.png)

The answer to this question can be found in the same xml file. I just searched for other instances where the rclone tool was used. Reading the rclone documentation we can understand that the first argument after copy is the folder we want to copy.

![image](https://user-images.githubusercontent.com/80063008/227508189-427a980b-2de0-4a3c-873f-c4ad2c28dcb8.png)

Question 6:  
![image](https://user-images.githubusercontent.com/80063008/227508372-b582806a-8547-4de9-af53-d7484deb5bd6.png)

From the same syntax as above, we understand that what we specify after remote is where we want to copy the folder to. In this case, the folder called exfiltration:

![image](https://user-images.githubusercontent.com/80063008/227508694-c9b6a044-6f8a-4394-866d-97c9a3104e21.png)

HTB{3v3n_3xtr4t3rr3str14l_B31nGs_us3_Rcl0n3_n0w4d4ys}


# Nightmare on Hunt Street

![image](https://github.com/user-attachments/assets/cf530e01-9d8c-46f4-aadf-a44237efc753)

Download: [logs-parts1-5.zip](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/logs-parts1-5.zip)

## My Solution

This is a group of questions where we need to figure out the answers from the provided Windows Event Viewer logs.  

![image](https://github.com/user-attachments/assets/fa24c5ef-b916-4b31-aa82-bfdedbfae004)

I'm sure that there are better ways to do this challenge however, what I usually do is I convert the `.evtx` files to something that is human readable. For this purpose I used the [EvtxECmd.exe](https://github.com/EricZimmerman/evtx) tool to convert the files to `.csv`.  

```bash
EvtxECmd.exe -f "C:\Temp\Application.evtx" --csv "c:\temp\out" --csvf MyOutputFile.csv
```

The data, or Payload, is all now in one column:  

![image](https://github.com/user-attachments/assets/bccfbfc7-483a-44d9-ad3f-394adbe2ba9c)

### Question 1: What is the IP address of the host that the attacker used?

Answer: `10.1.1.42`

![image](https://github.com/user-attachments/assets/0a7bfcae-2eb7-4fee-9eec-1748c63f6e9f)

### Question 2: How many times was the compromised account brute-forced? Answer just the integer value.

Answer: `32`

A quick google or just general knowledge tells us that brute force attacks can be identified by looking for the Event log failure Ids of `4625`:  

![image](https://github.com/user-attachments/assets/93ec28ca-5960-47d9-981b-b5877c22b927)

We filter those and can see the number of times this shows up in the logs.

### Question 3: What is the name of the offensive security tool that was used to gain initial access? Answer in all lowercase.

Answer: `psexec`

In the logs we can see a .exe binary with a random name which is a strong indicator of psexec. This tools creates these kinds of files when getting a foothold:  

![image](https://github.com/user-attachments/assets/9f13946f-aa46-48be-89e9-c7d6cf477bce)

### Question 4: How many unique enumeration commands were run with net.exe? Answer just the integer value.

Answer: `3`

I noticed the `net` command being used so I opened the .csv file in sublime and looked for unique instances of it being used.

First time it is used to enumerate the users on the machine:  

![image](https://github.com/user-attachments/assets/4cf8c826-8e3e-4d18-bacc-c15a61c67cc8)

Second time it is used to enumerate the groups on the machine:  

![image](https://github.com/user-attachments/assets/e29b7c55-3743-4fe7-a991-7ecd69e4dc72)

Third time it is used to enumerate the shares on the machine:  

![image](https://github.com/user-attachments/assets/a9538103-71fc-44e5-aa2e-4cd2f3c58f9e)

### Question 5: What password was successfully given to the user created?

Answer: `Susan123!`

We know that the EventID for a password reset is 4724 so when looking for it, we can only see one instance at 11:53.9:  

![image](https://github.com/user-attachments/assets/7ac0e0e4-0d0f-4eed-a631-72a2b1c53acc)

A quick look in the logs for activity around that time, we can see the password:  

![image](https://github.com/user-attachments/assets/28f91825-2b00-4baa-84bd-e40f1e0ae97d)


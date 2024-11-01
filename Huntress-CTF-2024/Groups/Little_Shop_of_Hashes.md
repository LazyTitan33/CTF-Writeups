# Little Shop of Hashes

![image](https://github.com/user-attachments/assets/56de7ad9-a989-4df3-badd-27ab9601e420)


Download: [little_shop_of_hashes_logs.zip](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/little_shop_of_hashes_logs.zip)


## My Solution

This is a group of questions where we need to figure out the answers from the provided Windows Event Viewer logs.  

I'm sure that there are better ways to do this challenge however, what I usually do is I convert the `.evtx` files to something that is human readable. For this purpose I used the [EvtxECmd.exe](https://github.com/EricZimmerman/evtx) tool to convert the files to `.csv`.  

```bash
EvtxECmd.exe -f "C:\Temp\Application.evtx" --csv "c:\temp\out" --csvf MyOutputFile.csv
```

### Question 1: What is the name of the service that the attacker ran and stopped, which dumped hashes on the first compromised host?

Answer: `Remote Registry`

In the System logs of HostB we can see the Remote Registry service having been run and stopped. This is a service that `secretsdump.py` starts and stops when dumping hashes.

![image](https://github.com/user-attachments/assets/30442b84-a00d-4a3a-83f8-30a84b8e65c3)

### Question 2: What lateral movement technique did the threat actor use to move to the other machine?

Answer: `Pass the Hash`

Since the attacker dumped hashes, it's logical to deduce that the attacker then used said hashes.

### Question 3: What is the full path of the binary that the threat actor used to access the privileges of a different user with explicit credentials?

Answer: `C:\\Users\\DeeDee\\Documents\\runasc.exe`

This can be seen in the Application logs of HostA.  

![image](https://github.com/user-attachments/assets/db4672ef-cab2-4829-9681-95c1bf02186b)

### Question 4: How many accounts were compromised by the threat actor?

Answer: `3`

In the Security logs from HOSTB and HOSTA, we filter based on EventID 4776 which is for NTLM authentication.

![image](https://github.com/user-attachments/assets/763d74d6-a73e-4c13-8e85-76afc1aab48f)

### Question 5: What is the full path of the binary that was used to attempt a callback to the threat actor's machine?

Answer: `C:\Users\DeeDee\Documents\nc.exe`

This can be seen in the Application logs of HostA:  

![image](https://github.com/user-attachments/assets/49311d56-0005-4489-bbbb-7e87f7b7edfa)

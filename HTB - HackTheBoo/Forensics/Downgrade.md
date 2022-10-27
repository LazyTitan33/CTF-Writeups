I solved this mostly by just applying my knowledge about Windows and Active Directory. Some were googleable as well. The Event logs weren't that helpful to me other than for the last two questions.

### 1. Which event log contains information about logon and logoff events? (for example: Setup)  
Answer: `Security`

![image](https://user-images.githubusercontent.com/80063008/198259644-70e3e12a-e5d2-4fcd-8df6-7e59a104b023.png)
![image](https://user-images.githubusercontent.com/80063008/198258987-1b169b7f-afb3-481b-bdbf-ba06552692e5.png)

### 2. What is the event id for logs for a successful logon to a local computer? (for example: 1337)  
Answer: `4624`

![image](https://user-images.githubusercontent.com/80063008/198259397-d2645378-9138-467a-9b5b-cbbac9bc4721.png)
![image](https://user-images.githubusercontent.com/80063008/198259274-2fdf6c68-4a1f-4c20-9eb0-6b77d1b6d1e0.png)

### 3. Which is the default Active Directory authentication protocol? (for example: http)  
Answer: `kerberos`

![image](https://user-images.githubusercontent.com/80063008/198260000-eb7e97d0-1966-453e-9ed7-3a5af2f3d4fd.png)
![image](https://user-images.githubusercontent.com/80063008/198260051-6e816eb9-ff14-459c-91e7-522fd5d8bb97.png)

### 4. Looking at all the logon events, what is the AuthPackage that stands out as different from all the rest? (for example: http)  
Answer: `NTLM`

Let's narrow things down by using the filter on the right side to see only successful logons as we assume a successful breach.

![image](https://user-images.githubusercontent.com/80063008/198262490-5a6a453f-0e3b-4a2f-a6b2-f25c81b934e7.png)

Looking through the first few entries in the Security.evtx file, we notice an NTLM authentication for Administrator. This entry is somewhere between a few Kerberos authentications so it clearly stands out. Why would the administrator log in with NTLM when Kerberos authentication should be used?!

![image](https://user-images.githubusercontent.com/80063008/198262715-602e0810-193c-4bda-a748-8c4df230a57f.png)
![image](https://user-images.githubusercontent.com/80063008/198260424-02272d28-f09f-4cba-96fa-c578737968f9.png)

### 5. What is the timestamp of the suspicious login (yyyy-MM-ddTHH:mm:ss) UTC? (for example, 2021-10-10T08:23:12)  
Answer: `2022-09-28T13:10:57`

We can switch to `XML View` to see the details including the timestamp. We need to ensure we copy only the format the question ask from us. We need to copy only until the seconds.

![image](https://user-images.githubusercontent.com/80063008/198260723-66c2bfac-d1e6-404a-b4aa-9487fb54d039.png)
![image](https://user-images.githubusercontent.com/80063008/198260773-cd05e968-3995-4af2-8e43-739e27354ed4.png)

HTB{4n0th3r_d4y_4n0th3r_d0wngr4d3...}

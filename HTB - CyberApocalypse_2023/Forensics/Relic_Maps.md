For the Relic Maps challenge, we already have a good starting point as the challenge description tells us directly where to go:

![image](https://user-images.githubusercontent.com/80063008/227509170-41ee6bf5-cf2d-4c49-9ef3-68a4561c71b8.png)

We add relicmaps.htb to our /etc/hosts file and make a get request for the specified OneNote file.

As usual, I like to first have a quick glance with `strings`. In this case we find a powershell command was executed to access another endpoint on the same domain:

![image](https://user-images.githubusercontent.com/80063008/227509405-426bb031-ddba-49eb-8c3f-30903f62c263.png)

We access it ourselves and we get a .bat file. This, however, is obfuscated.

![image](https://user-images.githubusercontent.com/80063008/227510055-563880fd-30a0-44bb-acc8-477a8dd07958.png)

It also has what looks like a base64 payload in it which seems encrypted:

![image](https://user-images.githubusercontent.com/80063008/227510114-ae15d3a6-fe2f-4516-a981-ce92b6ff6071.png)

It seems to exit at the end after everything gets executed:

![image](https://user-images.githubusercontent.com/80063008/227510377-6375e09b-fc00-4426-a2ce-11a434e97226.png)

I tried a dynamic deobfuscation approach. I removed the exit and added an echo statement at the last line in order to see it.

![image](https://user-images.githubusercontent.com/80063008/227510873-f6a10bbc-f1e4-45c0-98ce-e05bdf45617d.png)

After that, we run the .bat file in an isolated Windows VM and we get this output (I only recommend doing this with extreme caution, even in CTFs, you can still have active malware):

![image](https://user-images.githubusercontent.com/80063008/227513087-a2c550fd-6f7a-472b-a139-281c7a59ef1a.png)

It's still a bit difficult to read but we can see what matters. We see a `Key`, we see an `IV` and we see `gzip` being mentioned. Remember we have the Base64 payload we found earlier which is encrypted. 

We can now base64 decode it, then AES decrypt the content using the Key and IV we saw above. As expected, we have a gzip file.
![image](https://user-images.githubusercontent.com/80063008/227511709-124fce97-f55a-49b5-89a1-fe7889bbe198.png)

The recipe in the screenshot above is this one:

```
https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)AES_Decrypt(%7B'option':'Base64','string':'0xdfc6tTBkD%2BM0zxU7egGVErAsa/NtkVIHXeHDUiW20%3D'%7D,%7B'option':'Base64','string':'2hn/J717js1MwdbbqMn7Lw%3D%3D'%7D,'CBC','Raw','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)
```

After we save the file.gz and gunzip it, we get a .Net assembled file.
![image](https://user-images.githubusercontent.com/80063008/227511804-3a771932-6ab7-4bce-9e7d-d343cb6608c5.png)

We open this in dnSpy and find the flag:

![image](https://user-images.githubusercontent.com/80063008/227512344-ce54ac08-220c-44aa-af23-ce6f517ca6c4.png)

HTB{0neN0Te?_iT'5_4_tr4P!}

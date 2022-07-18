Challenge Description:

_We have been actively monitoring the most extensive spear-phishing campaign in recent history for the last two months. This campaign abuses the current crypto market crash to target disappointed crypto owners. A company's SOC team detected and provided us with a malicious email and some network traffic assessed to be associated with a user opening the document. Analyze the supplied files and figure out what happened.__

We get two files. A .doc and a .pcapng.

![image](https://user-images.githubusercontent.com/80063008/179471533-1bb43988-da7d-417d-aaf6-92c44635eb33.png)

Running a quick olevba on it, we can see a few strings reversed.

```bash
olevba --deobf mbcoin.doc
```

![image](https://user-images.githubusercontent.com/80063008/179471629-dfbd7c30-28b8-479e-9988-4a120c643245.png)

Over time I got pretty good at reading reversed texts. The interesting bit that can be seen is that it is executing a vbscript file.

```bash
cmd /k cscript.exe C:\ProgramData\pin.vbs
```

I went to https://any.run and put the .doc file there to run. I wanted to get the vbs script that it was running and see what was inside. If you are not familiar with https://any.run, when it runs files, if those create other files on the system, you can see that from the lower left by clicking on the little button.

![image](https://user-images.githubusercontent.com/80063008/179472382-68d43851-d412-4310-92a6-972b721b7233.png)

You can download these created files. Which is what I did for the pin.vbs file.

![image](https://user-images.githubusercontent.com/80063008/179472459-bed2729e-9fa3-4c9c-ba7c-7a00dfad69f4.png)

This file creates 5 dll files named www1.dll, www2.dll, www3.dll, www4.dll, www5.dll. It does so by downloaded them from some websites so we should see that in our wireshark capture.

Going to the protocol hierarchy, we see a large percentage of this capture consists of data capture via http. 

![image](https://user-images.githubusercontent.com/80063008/179473399-ecea7e93-a312-485d-a3c7-0f5886c2fc7d.png)

We can apply that as filter and we get 3 requests. The first was not found and the other two were 200 OK.

![image](https://user-images.githubusercontent.com/80063008/179473485-bce1a875-156a-48ea-92ab-bb23cdc0b5dc.png)

We follow the first one and it is a GET request to /vm.html.

![image](https://user-images.githubusercontent.com/80063008/179473649-c6df38c3-3cd8-4998-af1d-fe67c518e793.png)

We can see that in the vbscript, it corresponds to downloading www4.dll.

![image](https://user-images.githubusercontent.com/80063008/179473999-b6c7aa53-be90-43da-8ca0-5db1a4e49aae.png)

The 2nd one is a GET request to /pt.html.

![image](https://user-images.githubusercontent.com/80063008/179473920-d6bfc7d8-0078-4c74-a599-0dcc58591e86.png)

This coresponds to www1.dll.

![image](https://user-images.githubusercontent.com/80063008/179474065-7f0f8320-fd94-4e9d-8fc6-8e6830a5aad9.png)

In Wireshark, we can go to File - Export Objects - HTTP. And we can save both the vm.html and the pt.html files. If we run file in linux on these, we only get back that their data. Since we are stuck, let's take another look at the vbscript.

We see it is doing something with the files it downloaded but it's a bit tricky to read.

![image](https://user-images.githubusercontent.com/80063008/179475422-bf54092e-a8f3-4842-9e3d-56e21d51a45a.png)

I first separated the strings at the ; so I can more clearly see the individual variables and what they are doing.

![image](https://user-images.githubusercontent.com/80063008/179475670-e12ee4b0-41c5-44f5-8a47-b49de3739874.png)

Variable $b reads all bytes from the downloaded file in C:\ProgramData\www1.dll.  
Variable $k is just a string.  
Variable $r takes the length of variable $b which are the bytes of the dll file and uses a XOR operation with the $k string and its length.  
Then if length is greater than 0 it writes a new file in C:\ProgramData\www.dll.  

This is the same process for all dll files. All that is different is the $k string.

In my Command VM which is an isolated Windows VM machine, I modified the the $b variable for it to take the bytes from my file and then write it somewhere else.

```powershell
$b = [System.IO.File]::ReadAllBytes((('C:GPH'+'UsersGPHuserGPHdesktopGPH' + 'pt.ht'+'ml') -CrePLacE'GPH',[Char]92)); 
$k = ('6i'+'I'+'gl'+'o'+'Mk5'+'iRYAw'+'7Z'+'TWed0Cr'+'juZ9wijyQDj'+'KO'+'9Ms0D8K0Z2H5MX6wyOKqFxl'+'Om1'+'X'+'pjmYfaQX'+'acA6'); 
$r = New-Object Byte[] $b.length; for($i=0; $i -lt $b.length; $i++){$r[$i] = $b[$i] -bxor $k[$i%$k.length]};
if ($r.length -gt 0) {[System.IO.File]::WriteAllBytes((('C:Y9A'+'UsersY9AuserY9A' + 'file1.txt').REpLace(([chAr]89+[chAr]57+[chAr]65),[sTriNg][chAr]92)), $r)}
```

Then I ran it just like it is shown in the vbscript, with rundll32 and the ldr argument. 

![image](https://user-images.githubusercontent.com/80063008/179477071-17675122-05c8-41aa-ba85-e6e037310e98.png)

It pops open a dialog box.

![image](https://user-images.githubusercontent.com/80063008/179476742-713a7390-f8b4-48dd-bba4-868894cb062b.png)

Nothing in the first file but when I repeated the steps for the second file, I got the flag.

![image](https://user-images.githubusercontent.com/80063008/179476864-8725c8fb-0fb6-4979-8f37-8a5247fdf6ff.png)

HTB{wH4tS_4_sQuirReLw4fFl3?}


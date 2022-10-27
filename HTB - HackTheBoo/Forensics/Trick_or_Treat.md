With strings we see a lot of DNS requests with a hex string in the subdomain:

![image](https://user-images.githubusercontent.com/80063008/198271579-a7160e6f-fd59-4f1b-adef-68cc2b78419f.png)

So there's been some DNS exfil done here. Carved it out with tshark and some awk action. I'm sure only tshark could've been used but I'm not that familiar with it and I was in a hurry. We can output the result into a file and see what it is.

```bash
tshark -r capture.pcap -Y 'dns.resp.name'|awk '{print $13}'|awk -F "." '{print $1}' |xxd -r -p > mysterfile
````
![image](https://user-images.githubusercontent.com/80063008/198272011-e132d952-f835-4ee4-b63b-6a3991a309f6.png)

Looks like an Excel file. Let's open it (always be careful and take precautions when opening such files from the internet).

![image](https://user-images.githubusercontent.com/80063008/198272094-e1aaa5cc-4597-4ddb-98d4-96fe2e6b3c9c.png)

HTB{M4g1c_c4nn0t_pr3v3nt_d4t4_br34ch}

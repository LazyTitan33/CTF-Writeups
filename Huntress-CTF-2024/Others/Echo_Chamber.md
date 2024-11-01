# Echo Chamber

![image](https://github.com/user-attachments/assets/d1f75992-40e4-45f0-b120-92a115c2e051)

Download: [echo_chamber.pcap](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/echo_chamber.pcap)

## My Solution

The provided pcap file contains ICMP traffic:  

![image](https://github.com/user-attachments/assets/0269335e-3e96-499a-88ef-37adf1902174)

Using tshark I exfiltrated only the requests (type 8):  

```bash
tshark -r echo_chamber.pcap -Y "icmp.type == 8" -T fields -e data
```

And saw repeating values:  

![image](https://github.com/user-attachments/assets/60a2d7f6-b61f-4e38-ab0f-a71ac47987e6)

So I decided to take just the first 2 characters which look like hex and decode them:  

```bash
tshark -r echo_chamber.pcap -Y "icmp.type == 8" -T fields -e data 2>/dev/null|sed 's/^\(.\{2\}\).*/\1/'|xxd -r -p
```
The result was a PNG file based on the header:  

![image](https://github.com/user-attachments/assets/b60f61db-9e2c-4a6a-9e4f-a2e7aba1ecf2)

And we have our flag:  

![image](https://github.com/user-attachments/assets/cee6c2c9-22e3-4a3b-8555-dbb12bf6ff04)

`flag{6b38aa917a754d8bf384dc73fde633ad}`

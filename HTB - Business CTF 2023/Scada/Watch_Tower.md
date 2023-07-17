### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c1efa2f9-6af9-4501-9f2a-42d0c9420c5c)

We get a wireshark capture for this challenge. The capture contains modbus traffic with multiple `Write Multiple Registers` functions. The `Reference Numbers` look to be decimals:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/50436850-ecd5-4d7a-8235-4a4a5ab29eea)

We can use the syntax below with tshark to carve all of them out:

```bash
tshark -r tower_logs.pcapng -Y "modbus" -T fields -e modbus.reference_num|grep .|awk '{print $1}' ORS=' '
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5287e38b-1867-4bdf-b255-197ce6c38159)

After converting from Decimal using Cyberchef, we get the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/92d9c1e2-9b1f-4662-94c4-c552e67b9b89)

HTB{m0d8u5_724ff1c_15_un3nc2yp73d!@^}

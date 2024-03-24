# wifiland

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/702f43a6-1788-481f-82a3-0b67c1f5fca7)

# Solution

The wireshark capture contains an [EAPOL handshake](https://networklessons.com/cisco/ccnp-encor-350-401/wpa-and-wpa2-4-way-handshake) so we can try to crack the password using [aircrack-ng](https://www.aircrack-ng.org/):  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6a66eae0-c06c-4bda-a505-47708b892f6e)

```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b '02:00:00:00:05:00' wifiland.cap
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2cb60866-9208-4138-a471-f6c664d37cbd)

We can now use this password to decrypt the traffic by going in Wireshark in `Edit` -> `Preferences` -> `Protocols` -> `IEEE - 802.11` -> `Edit` on Decryption Keys and set the password for `wpa-pwd`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c69e04ea-0879-4e65-b323-c363f01af15c)

Scrolling through the decrypted traffic we can eventually see an ARP broadcast request giving us the Client and Target IPs.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cb49235c-4aee-4dba-9cda-93f9d27b9eb7)

And we can now generate the flag:  

```python3
from hashlib import sha256

ip_client = "10.0.3.19"
ip_target = "93.184.216.34"

def calculate_sha256(ip_client, ip_target):

    input_string = ip_client + ip_target
    
    hash_result = sha256(input_string.encode()).hexdigest()
    
    return hash_result

sha256_sum = calculate_sha256(ip_client, ip_target)

print('CTF{'+sha256_sum+'}')
```

`CTF{b67842d03eadce036c5506f2b7b7bd25aaab4d1f0ec4b4f490f0cb19ccd45c70}`

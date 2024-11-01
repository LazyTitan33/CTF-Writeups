# Keyboard Junkie

![image](https://github.com/user-attachments/assets/8c4ea730-f8d5-41a0-8c18-49cb4ec7714b)

Download: [keyboard_junkie](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/keyboard_junkie)


## My Solution

When opening the provided file in Wireshark, I could see USB traffic. I've done these kinds of challenges in the past but couldn't remember the tool so I googled it:  

![image](https://github.com/user-attachments/assets/521d0942-96a6-4332-acbf-17d9b2961d19)

Using [this](https://github.com/TeamRocketIst/ctf-usb-keyboard-parser) tool allows us to decode keyboard traffic, but first we need to extract the traffic:  

```bash
tshark -r keyboard_junkie -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata  | sed 's/../:&/g2' >usbPcapData
```

Here we are using tshark to extract just the USB packets that have a length of 8 and are placing : every two characters to get a format recognized by the tool.

We then use the [ctf-usb-keyboard-parser](https://github.com/TeamRocketIst/ctf-usb-keyboard-parser) and get the flag:  

![image](https://github.com/user-attachments/assets/8977cec2-d6bb-4086-9ce2-fa84ceacb994)

Another easier method would be to use this other [parser](https://github.com/5h4rrK/CTF-Usb_Keyboard_Parser) which allows us to pass the wireshark capture directly and it will grab the traffic on its own:  

![image](https://github.com/user-attachments/assets/6b123389-47ea-4ecf-9208-06c962c23bcd)

`flag{f7733e0093b7d281dd0a30fcf34a9634}`

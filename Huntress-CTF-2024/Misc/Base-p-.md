# Base-p-

![image](https://github.com/user-attachments/assets/4fa9d0b1-4355-4a9d-afeb-61f42bd9db31)

Download: [based.txt](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/based.txt)

## My Solution

The provided text file has the following contents:  

![image](https://github.com/user-attachments/assets/88712c84-5248-4478-9d39-5f15036a7b86)

Which reminded me of the [BaseFFFF+1](https://github.com/LazyTitan33/CTF-Writeups/blob/main/Huntress-CTF-2023/Warmups/BaseFFFF%2B1.md) from last year's Huntress CTF.

So we can use [this](https://www.better-converter.com/Encoders-Decoders/Base65536-Decode) service to decode the Base65536 blob. 

![image](https://github.com/user-attachments/assets/e33ca54f-81d5-4053-8fd8-a575ff19f2e5)

We successfully decode the blob. This confirms we have the correct decoding. 65536 happens to also be the full range of ports which you can scan for using nmap with the `-p-` flag which is part of the challenge title.

We now have this base64 blob:  

```text
H4sIAG0OA2cA/+2QvUt6URjHj0XmC5ribzBLCwKdorJoSiu9qRfCl4jeILSICh1MapCINHEJpaLJVIqwTRC8DQ5BBQ0pKtXUpTej4C4lBckvsCHP6
U9oadDhfL7P85zzPTx81416LYclYgEAOLgOGwKgxgnrJKMK8j4kIaAwF3TjiwCwBejQQDAshK82cKx/2BnO3xzhmEmoMWn/qdU+ntTUIO8gmOw438
bbCwRv3Y8vE2ens9y5sejat497l51sTRO18E8j2aSAAkixqhrKFl8E6fZfotmMlw7Z3NKFmvp92s8+HMg+zTwaycvVQlnSn7FYW2LFYY0+X18JpB9
LCYliSm6LO9QXvfaIbJAqvNsL3lTP6vJ596GyKIaXBnNdRJahnqYLnlQ4d+LfbQ91vpH0Y4NSYwhk8tmv/5vFZFnHWrH8qWUkTfgfUPXKcFVi+5V
lx7V90OjLjZqtqMMH9FhMZfGUALnotancBQAA
```

When we parse this with [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)Gunzip()Render_Image('Raw')&input=SDRzSUFHME9BMmNBLysyUXZVdDZVUmpIajBYbUM1cmliekJMQ3dLZG9ySm9TaXU5cVJmQ2w0amVJTFNJQ2gxTWFwQ0lOSEVKcGFMSlZJcXdUUkM4RFE1QkJRMHBLdFhVcFRlajRDNGxCY2t2c0NIUDYKVTlvYWREaGZMN1A4NXp6UFR4ODE0MTZMWWNsWWdFQU9MZ09Hd0tneGduckpLTUs4ajRrSWFBd0YzVGppd0N3QmVqUVFEQXNoSzgyY0t4LzJCbk8zeHpobUVtb01Xbi9xZFUrbnRUVUlPOGdtT3c0MzgKYmJDd1J2M1k4dkUyZW5zOXk1c2VqYXQ0OTdsNTFzVFJPMThFOGoyYVNBQWtpeHFocktGbDhFNmZaZm90bU1sdzdaM05LRm12cDkyczgrSE1nK3pUd2F5Y3ZWUWxuU243RllXMkxGWVkwK1gxOEpwQjkKTENZbGlTbTZMTzlRWHZmYUliSkFxdk5zTDNsVFA2dko1OTZHeUtJYVhCbk5kUkphaG5xWUxubFE0ZCtMZmJROTF2cEgwWTROU1l3aGs4dG12LzV2RlpGbkhXckg4cVdVa1RmZ2ZVUFhLY0ZWaSs1VgpseDdWOTBPakxqWnF0cU1NSDlGaE1aZkdVQUxub3RhbmNCUUFB&oeol=VT) we get an image:  

![image](https://github.com/user-attachments/assets/edb684ba-1993-4ea9-b7fe-7be1459520cf)

Googling around for similar CTFs trying to figure out what we can do with this image, we find [something](https://rg27.medium.com/deadface-2023-color-me-impressed-writeup-0d74217f3f82) similar:  

![image](https://github.com/user-attachments/assets/af981ec0-2053-421b-8781-8075f33aa656)

So we go through a similar process of using [imagecolorpicker](https://imagecolorpicker.com/) and end up getting this string:

```text
#666c61#677b35#383663#663863#383439#633937#333065#613762#323131#326666#663339#666636#617d20
```

Decoding it with [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=IzY2NmM2MSM2NzdiMzUjMzgzNjYzIzY2Mzg2MyMzODM0MzkjNjMzOTM3IzMzMzA2NSM2MTM3NjIjMzIzMTMxIzMyNjY2NiM2NjMzMzkjNjY2NjM2IzYxN2QyMA) we get the flag:  

![image](https://github.com/user-attachments/assets/5ea77fa3-0548-4a85-a005-da7308c43a61)

flag{586cf8c849c9730ea7b2112fff39ff6a}

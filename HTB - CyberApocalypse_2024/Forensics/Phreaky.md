# Phreaky

## Enumeration
This one was a source of frustration because of my lack of proper scripting skills, but I got there in the end... perhaps with a bit of luck. We start off with a wireshark capture:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c166b89e-2647-4e66-922e-f42ad85eb9e2)

TCP stream 1 starts off strong showing us an email communication, saying this is the first part of the file and it has a password:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e7280d54-fb9b-462e-9347-fd5e65285155)

Decoding the Base64 blob, we find it's a zip file which we can unzip using the password:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/efcc1134-5977-4bb2-b161-2ed9fd54309c)

And we get a PDF file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e813ea73-ae2a-4bba-b09e-69a91ecd4bc3)

But we can't open it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d6079d4a-d2c2-43b6-b722-b25c8ae53d33)

As the email message said, and the filename says, this is the first part of the file. That means there has to be others.

The 3rd TCP Stream confirms we get another file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/01366bac-29fb-4869-b450-412e8cfb1560)

Given that there are somewhere around 30 TCP Streams, we can't do this manually. I mean, it's doable, but it's a lot of pain.

## Solution
Let's start by collecting all the passwords. Since it's plaintext traffic we can use strings and grep:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2871dfaf-dac8-4f77-bd1e-4a5a3a652a40)

There's 14 passwords so that means we will have to get 14 base64 blobs from the traffic, Base64 decode them, unzip them and patch them all together into one PDF. Easier said than done.

I started by using tshark to get all the media fiels where the base64 blobs are:

```bash
tshark -r phreaky.pcap -Y "tcp.stream % 2 == 1" -T fields -e media.type |grep . > extracted.hex
```
Using some bash, we can hex decode the extracted media fields and put them one by one in it's own file but we need to keep track of the order so we start from 01 to 14.

```bash
count=0; while read -r line;do ((count++)); printf -v padded_count "%02d" "$count";echo $line|xxd -r -p > files/$padded_count.b64;done <extracted.hex
```
Good, now we have 14 base64 blobs:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/718ac9fd-927e-4a34-ab1f-06b167e33bdd)

Now, for each one of them, we need to Base64 decode them and then unzip the result with the correct password and save the output. Another piece of bash scripting to do all of that:  

```bash
#!/bin/bash

# Assuming the files are in the folder named "files"
folder_path="files"
wordlist="passwords"  # Path to your wordlist file

# Initialize counter for wordlist lines
line_count=0

# Iterate through each file in the folder
for file in "$folder_path"/*; do
    # Check if the current item is a file
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        base64 -d "$file" > "$file.zip"
        
        # Increment line counter
        ((line_count++))

        # Extract the filename without extension
        filename=$(basename "$file")
        filename="${filename%.*}"

        # Get the password from the wordlist based on the line count
        pass=$(sed -n "${line_count}p" "$wordlist")
        
        # Unzip the file with the corresponding password from the wordlist
        unzip -P "$pass" "$file.zip"
        rm files/*.zip
        mv phreaks_plan* pdfs/

    fi
done
```
Then I started reading each file and placing it at the end of the first one. I couldn't think of a better way and at this point I was super tired from a days work and also doing other challenges.

cat phreaks_plan.pdf.part2 >> phreaks_plan.pdf.part1  
cat phreaks_plan.pdf.part3 >> phreaks_plan.pdf.part1  
cat phreaks_plan.pdf.part4 >> phreaks_plan.pdf.part1  
cat phreaks_plan.pdf.part5 >> phreaks_plan.pdf.part1  
etc  

Now I had 1 big PDF but... I couldn't read it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b977f7a5-f1fb-4bc3-8eb9-d811868acbf2)

I knew I must've messed something up in my process which was very hacky and dumb. I couldn't be bothered to try and script this properly in python so I searched online for ways to try and repair my PDF:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e0a41e3e-7e82-4209-8e04-20d5cc4a0442)

The first one didn't work. Luckily, the [second](https://www.freepdfconvert.com/repair-pdf) one provided a readable PDF and I got the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/31f153bb-d22b-4e5b-bc1b-d95c3b0b5b56)

This was an interesting challenge although a bit tedious. There's no mystery just implementation. I'm curious to see a proper fully scripted solution to this.

`HTB{Th3Phr3aksReadyT0Att4ck}`

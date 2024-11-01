# 1200 Transmissions

![image](https://github.com/user-attachments/assets/98fb4df7-7ede-4a52-8c09-4c9398c4bd42)

Download: [transmissions.wav](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/transmissions.wav)

## My Solution

A quick google search for similar challenges yealds a promising [result](https://ctftime.org/writeup/23189):  

![image](https://github.com/user-attachments/assets/5dd2f4e4-2946-4a3b-9452-ae7dd44b6af6)

So we install and run the same tool:  

```bash
sudo apt install minimodem
minimodem -r -f transmissions.wav 1200
```

And we get the flag:  

![image](https://github.com/user-attachments/assets/7a7f3429-b0b3-4d89-b55a-c5b1655e4ec7)

`flag{f28d133e7174c412c1e39b4a84158fa3}`

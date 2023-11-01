# Book By Its Cover

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/33e93054-d1c3-4054-b9d8-ac66daf17e49)

### Solution
This is a challenge that indicates the importance of common commands such as `file`. This doesn't apply just in CTFs.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e015e05c-51ec-4882-a452-52b876945f4f)

Because we now know that the "archive" is in fact a picture, we rename it.

```bash
mv book.rar book.png
```
Opening the picture, we get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c3f5ec92-3b11-47f1-ab43-657e91e09bf3)

To make it easier on us, we can use `tesseract`, a great OCR tool, to get the text out of the picture since we don't want to make any mistakes when manually transcribing it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c245d93b-1a51-4563-95ff-ca84a1a2e7d8)

This creates a flag.txt file containg our flag.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b38e63ed-fe67-4756-93fc-ca65b095de58)

flag{f8d32a346745a6c4bf4e9504ba5308f0}

# Babel

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4de8bc85-c09a-4fe8-a934-c2e0e7097502)

### Solution
The file provided seems to contain some obfuscated C# code:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d0abcc14-3676-4979-b0e6-b07c722a99a0)

I started adjusting the lines to make it more readable for me:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/61c41b92-6794-43cc-9a6f-d658c79fddbe)

At a first glance we can see that the first function is applied to the base64blob with the random characters (key) then the blob is Base64 decoded:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f672dee8-4ee6-4db8-bd12-c98dfc22254a)

I asked ChatGPT to rewrite that function in python3 and then I applied it to the blob and Base64 decoded it. After that, we write the resulted bytes into a file we call "decoded_assembly.dll":

```python3
import base64

def custom_function(t, k):
    bnugMUJGJayaT = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    WgUWdaUGBFwgN = ""
    ornBLfjI = dict(zip(k, bnugMUJGJayaT))

    for char in t:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            WgUWdaUGBFwgN += ornBLfjI.get(char, char)
        else:
            WgUWdaUGBFwgN += char

    return WgUWdaUGBFwgN


base64_blob = "base64blob";
key = "lQwSYRxgfBHqNucMsVonkpaTiteDhbXzLPyEWImKAdjZFCOvJGrU";

file = base64.b64decode(custom_function(base64_blob, key))

with open("decoded_assembly.dll", "wb") as fp:
        fp.write(file)
```

After we run the script, indeed a .dll file was created and we have a valid file which seems to be a .Net assembly.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4fe7796a-01f8-41a6-b7b8-76d6dfc90a19)

I wanted to check it in dnSpy but first, as always with any CTF challenge, we run strings on it and actually get the flag, no need for further reversing:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bb6bd035-d7f2-4d34-94b1-8422dc26689f)

flag{b6cfb6656ea0ac92849a06ead582456c}

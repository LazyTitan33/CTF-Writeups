# Tragedy Redux

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ff7a9fea-3e1f-4c27-8a78-69aed9e18369)

### Solution
This was the original description of the `Tragedy` challenge. They had to reupload the file and make this challenge. Running file on the provided file we can see it's an archive:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/05910d2a-52cc-40df-9ec9-b49e5fcce5c2)

However, running `unzip` with the `-l` flag to simply list the contents without decompressing it, we can see that in fact this is a Windows Word file. I opened the document in a segregated Windows VM and then looked at the Macros for AutoOpen that it had. Some interesting code was found with lots of fruits. The first function seems to be simply doing a subtraction of 17 from something. That's good to keep in mind.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2c0d56f4-a66e-49eb-8e53-332773482289)

The function called `Tragedy` seems to be the important one as it bares the name of the challenge and has some decimal strings in it.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5c0d27ea-9205-4114-bfc1-1dd8beebf2eb)

The long one is: 
```
129128136118131132121118125125049062118127116049091088107132106104116074090126107132106104117072095123095124106067094069094126094139094085086070095139116067096088106065107085098066096088099121094101091126095123086069106126095074090120078078
```
We entered this long string in Cyberchef and split it in groups of 3:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0d2639c0-2d61-4835-87ca-1af763569ee4)

Using python3, we then subtracted 17 from each group and converted it to ASCII:  

```python3
# Your original string of numbers
original_string = "129 128 136 118 131 132 121 118 125 125 049 062 118 127 116 049 091 088 107 132 106 104 116 074 090 126 107 132 106 104 117 072 095 123 095 124 106 067 094 069 094 126 094 139 094 085 086 070 095 139 116 067 096 088 106 065 107 085 098 066 096 088 099 121 094 101 091 126 095 123 086 069 106 126 095 074 090 120 078 078"

# Split the string into a list of numbers
numbers = original_string.split()

# Subtract 17 from each number and convert back to ASCII
result_string = "".join(chr(int(num) - 17) for num in numbers)

print(result_string)
```
The subtraction gives this output: 

```
112 111 119 101 114 115 104 101 108 108 032 045 101 110 099 032 074 071 090 115 089 087 099 057 073 109 090 115 089 087 100 055 078 106 078 107 089 050 077 052 077 109 077 122 077 068 069 053 078 122 099 050 079 071 089 048 090 071 082 050 080 071 089 082 104 077 084 074 109 078 106 122 085 068 099 109 078 057 073 103 061 061
```

Running the python script is successfully and we get a string, a powershell command with the payload Base64 encoded:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/00889687-03c9-4bab-8373-b637b9039215)

We modify the script to account for that and print out the flag directly:  

```python3
import base64

# Your original string of numbers
original_string = "129 128 136 118 131 132 121 118 125 125 049 062 118 127 116 049 091 088 107 132 106 104 116 074 090 126 107 132 106 104 117 072 095 123 095 124 106 067 094 069 094 126 094 139 094 085 086 070 095 139 116 067 096 088 106 065 107 085 098 066 096 088 099 121 094 101 091 126 095 123 086 069 106ll
l 126 095 074 090 120 078 078"

# Split the string into a list of numbers
numbers = original_string.split()

# Subtract 17 from each number and convert back to string
result_string = "".join(chr(int(num) - 17) for num in numbers)

print(base64.b64decode(result_string.split(' ')[2]).decode().split('"')[1])
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c6a810ca-bf30-461b-9f4c-9e8e547f94d3)

flag{63dcc82c30197768f4d458da12f618bc}



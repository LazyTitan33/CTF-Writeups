![image](https://user-images.githubusercontent.com/80063008/166220014-01c95cab-cc2d-4c2e-9882-fff645883735.png)

Reading the file we are given, we see a bunch of hex. 

![image](https://user-images.githubusercontent.com/80063008/166220052-fd8c4168-edaf-434e-9d0c-1554c16b0a03.png)

We can use sed to remove the \x so we can use xxd in the terminal to convert the hex.

`cat quirky|sed 's/\\x//g'|xxd -r -p`

Based on the file header, we can tell this is supposed to be a PNG file.

![image](https://user-images.githubusercontent.com/80063008/166220232-0bf49fa6-de76-40d8-89d2-58bf1101a59a.png)

Redirecting that output to a file, we can see it's a QR code.

![image](https://user-images.githubusercontent.com/80063008/166220554-13d58a02-f262-4069-8fbf-f1cb14ed299b.png)


We can decode QR codes directly in the terminal using zbarimg. So putting it all together, we can use a bash onliner to get the flag.

`cat quirky|sed 's/\\x//g'|xxd -r -p > pic.png|zbarimg -q pic.png|awk -F ":" '{print $2}'`

![image](https://user-images.githubusercontent.com/80063008/166220479-96f3adc7-203d-4c78-a263-de8cf854f1c0.png)


# qrrr

We are given a picture of a QR code.

![image](https://user-images.githubusercontent.com/80063008/136173535-423a8857-3945-4d68-b7d3-286db97e7188.png)


└─$ zbarimg flag.png                                                                                       
QR-Code:5ff8d4e4958d8007a3897}  

Zbarimg sees the end of a potential flag given the curly brace.

Put the the file into stegsolve.jar and navigated through all the layers.

Found another two qr codes:

![image](https://user-images.githubusercontent.com/80063008/136173554-055fb13f-1d4f-44ac-965a-d07b549d1325.png)


└─$ zbarimg solved.bmp 
QR-Code:12d99aa3a92f1abbb7d40786

And

![image](https://user-images.githubusercontent.com/80063008/136173577-f5eb1cae-2e2c-4c41-989b-277055a40915.png)


└─$ zbarimg solved2.bmp 
QR-Code:SNYK{6947bd4818ffc1768f2

Putting the three together we get the flag.


Flag: SNYK{6947bd4818ffc1768f212d99aa3a92f1abbb7d407865ff8d4e4958d8007a3897}

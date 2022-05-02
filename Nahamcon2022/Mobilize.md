![image](https://user-images.githubusercontent.com/80063008/166224279-85ebc6d2-611a-4078-9be5-2190141efc45.png)

To decompile the apk file we can use a tool call jadx.

`sudo apt install jadx`  
`jadx -d /tmp/decompiled_folder /tmp/mobilize.apk`

We can do a recursive grep search and we quickly find the flag:

`grep -Rn "flag{.*}"`

![image](https://user-images.githubusercontent.com/80063008/166224542-862b4d90-6c8f-4198-877b-b0180b24ea46.png)

It is in /resources/res/values/strings.xml

![image](https://user-images.githubusercontent.com/80063008/166224597-29732781-469b-498c-92ff-854b5de64214.png)

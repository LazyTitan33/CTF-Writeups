# Backdoored Splunk II

![image](https://github.com/user-attachments/assets/9e700c40-b597-40a9-8196-809fd7f894bf)

Download: [Splunk_TA_windows.zip](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/Splunk_TA_windows.zip)

## My Solution

This is very similar with the [Backdoored Splunk](https://github.com/LazyTitan33/CTF-Writeups/blob/main/Huntress-CTF-2023/Forensics/Backdoored_Splunk.md) challenge from last year. This time if we find something suspicious in the `dns-health.ps1` file:  

![image](https://github.com/user-attachments/assets/52f5eb82-1d80-4727-b125-c74fe7ca5105)

We see a bunch of bytes being joined together and then passed to IEX. I changed that to pass it to echo instead and reveal a base64 blob:  

![image](https://github.com/user-attachments/assets/148147f3-4f30-4853-9f04-f42763219b04)

When decoding that further, we can see it doing an Invoke-WebRequest with a specific Authorization Basic header and some base64 encoded credentials. We just need to do the same request and replace the port with the one given by the challenge and we get our flag:

```bash
curl -s -u backdoor:this_is_the_http_server_secret http://challenge.ctf.games:32557|awk '{print $2}'|base64 -d|awk '{print $2}'
```

![image](https://github.com/user-attachments/assets/961a2607-de9c-4a49-a4de-a32d81b844dd)

`flag{e15a6c0168ee4de7381f502439014032}`

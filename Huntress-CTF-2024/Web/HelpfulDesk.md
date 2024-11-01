# HelpfulDesk

![image](https://github.com/user-attachments/assets/56e7b831-887f-4516-bf30-f0039d57542d)

## My Solution

When accessing the page, we get a login screen with a yellow banner saying that a Security Update is required:  

![image](https://github.com/user-attachments/assets/d8b54efc-5cb2-4dc9-a210-2b263ac5c531)

Looking at the security bulletin, we find a Critical Severity update in version 1.2. So we download the source code, as well as the source code for v1.1 so we can see the difference and check out what they patched:  

![image](https://github.com/user-attachments/assets/6e5ff531-a43d-4ed0-a34e-21dc7cd3ed31)

It's a .Net application and in the `SetupController` for version 1.1 we see it checking the `/Setup/SetupWizard` endpoint:  

![image](https://github.com/user-attachments/assets/7ec7f959-7770-4211-b916-72ecdd2d280c)

However, in version 1.2, they are now trimming the `/` at the end of the URL, if there is one.  

![image](https://github.com/user-attachments/assets/fe550316-7a4f-4fb1-8ded-13a0e5023a79)

We also notice where the flag is supposed to be, in one of the Clients of the service.  

![image](https://github.com/user-attachments/assets/7583283a-15a9-4eaa-805d-50820e24f97a)

Considering they are running the unpatched version, we can navigate to `/setup/setupwizard/` with a slash at the end, and we end up on the Setup Wizard where we can setup an administrator account:  

![image](https://github.com/user-attachments/assets/1f7e7ad9-e70b-4b78-b0dd-1a3b9965c671)

We access the client we noticed in the source code and download the flag.  

![image](https://github.com/user-attachments/assets/3b02da72-9076-458b-ab93-bd3a9187cbf2)

`flag{03a6f458b7483e93c37bd94b6dda462b}`

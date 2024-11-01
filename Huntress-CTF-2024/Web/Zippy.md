# Zippy

![image](https://github.com/user-attachments/assets/e2797b91-4a25-4fe4-b2ca-2800697a8321)

## My Solution

The about page of the provided website mentions it is using `Razor Pages` and most importantly, it is running with `runtime compilation` which means that Razor views can be edited on the server while the application is running, and changes take effect immediately without needing to redeploy the application.  

![image](https://github.com/user-attachments/assets/16e074eb-0706-4594-a6c8-86d16de9dd7e)

We also have the option to upload a ZIP file:  

![image](https://github.com/user-attachments/assets/cf3236ea-dd55-41e7-904b-294b6380dd73)

When uploading a Zip file, I modified the path to the absolute path of the application:  

![image](https://github.com/user-attachments/assets/b771407d-c863-4f1b-b4d8-0f979a8ebd5a)

In the /Browse endpoint we can list the contents of arbitrary directories, including the one of the app and we can confirm that our file was uploaded:  

![image](https://github.com/user-attachments/assets/df1c07d2-8eb4-4e3a-98c7-3b08a8eb403a)

In this situation, we would need to replace a `.cshtml` file that is rendered by the application. These can be found in the /app/Pages directory:  

![image](https://github.com/user-attachments/assets/2b457919-d714-4b27-958a-c685c7ea52d1)

My target was the Privacy endpoint since it didn't contain any functionalities required for the application so I couldn't break anything.  

After a few attempts of trying to get RCE I went the simpler route and just read the flag into the page with the code below:  

```html
@page
@using System.IO
@{
    string fileContent = string.Empty;
    fileContent = System.IO.File.ReadAllText("/app/flag.txt");
}
<div>
    <h2>Flag Content:</h2>
    <p>@fileContent</p>
</div>
```

I base64 encoded this and uploaded it then reloaded the /Privacy endpoint.

![image](https://github.com/user-attachments/assets/8c2afb5e-5c5e-4486-ae0f-21fa3b26b510)

`flag{a074eb7973c4c718790baefc096654dd}`

# ElectronBuzz

This was probably the unintended way of getting the flag because it was super easy however despite that, the challenge had very few solves. The expected way was probably to reverse engineer or decompile it.

We were given the option to download an installer either for MacOS (.dmg), for Windows (.exe) or Linux (.deb).

I downloaded the .exe app and installed it in Windows.

Went in the location where it was installed and opened various files in Notepad++.

In the resources folder, there was a file called app.asar which contained the hardcoded flag 

![image](https://user-images.githubusercontent.com/80063008/136174633-5252cb01-a415-45f7-944f-75dae64f6153.png)


Flag: SNYK{07cd77795145aa60a36693f31fcf660c4f1ff2bae64e084fc1bbbc3affcc51eb}

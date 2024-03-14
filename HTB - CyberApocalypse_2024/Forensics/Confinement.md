# Confinement

## Solution

For this challenge, the description actually helps us a bit, giving us a starting point for the enumeration:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/937e8f15-a784-4856-81e4-8bb10c896c0d)

The received file is a `.ad1` file which can be opened with [FTK Imager](https://www.exterro.com/ftk-product-downloads/):  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/154617b0-2d92-407d-98b0-43240cea9fcd)

In the indicated folder, we can see a .hta file and a .korp file which is a non-standard file extension.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/06d83c44-c6fc-47eb-8f25-353893841b10)

The .hta is actually a ransomware note.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9b3053e0-e262-405f-a9e4-b256a29d21d5)

In this we can find an ID which we'll save for later.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3e322ddd-6fa7-461b-afbe-7fd5f4151ac7)

A ransomware should normally be detected by Windows Defender, there should be a way for it to have landed on the machine, maybe it was downloaded, maybe it was launched with powershell etc. We need to look at the Windows Event logs and see if they caught something, hopefully they weren't encrypted as well. The default location where the logs are saved is in `%systemroot%\system32\winevt\logs`. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5eb24548-1fbf-478a-9060-a7c3f9f36189)

Luckily the logs weren't encrypted and we can export them from the image:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/28d88fe0-b4d4-4e26-86e8-ecb0010f508c)

Rather than opening these one by one and looking through them manually, we can use this [evtx](https://github.com/omerbenamram/evtx/releases/tag/v0.8.0) tool to convert them into an xml format that we can plainly read and grep through. I parsed each file and saved it in a different folder with this syntax:  

```bash
for file in logs/*.evtx;do ./evtx_dump-v0.8.0-x86_64-unknown-linux-gnu "$file" > logs_decoded/"${file%.evtx}.xml";done
```
Looking through the Powershell log to see what commands were executed, we notice a `./intel.exe` file being run which is non-standard.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6f7596d5-d991-43ee-957a-d8dd26ce1d47)

This was run shortly after this browser password decrypter which is a known tool.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8c4f6aa-4647-42da-8df6-55d61bdff5c0)

So, they stole the target's browser passwords then encrypted the files. It makes sense for a ransomware attack. Grepping for `intel.exe` we can see that Defender seems to have caught it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12f14766-c179-43a5-90c1-0de5f7a3d7a1)

Windows Defender quarantines files in `c:\programdata\microsoft\windows\defender\quarantine`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6930d038-23e8-4bdb-baae-8ab60d7c1963)

However they are encrypted:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f3a04771-8030-4831-9a3b-4ab2d13f784a)

Googling how do decrypt these, we find a helpful github [gist](https://gist.githubusercontent.com/OALabs/30346d78a1fccf59d6bfafab42fbee5e/raw/b2464fc6a1e758f3bff122e10ae3e1cb48a5027c/windows_defender_unquarantine.py):  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e74012eb-59fd-43ef-a54b-c4204059ff09)
After we export the quarantined files, we run the script and recover the executable that was ran.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/68596697-7c8a-45ee-8f92-d5ee45313b3b)

It seems to be a `.Net` binary:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ddf02416-1b9e-4044-be6c-4158fd6365aa)

Running strings on it, we can confirm that this was the culprit as we can see the ransom note in it.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/446114f1-c5d4-41ba-82f3-31c8a5008852)

Decompiling the executable in dnSpy, we can see an Encrypter and Encrypter.Class:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1429e139-f5ed-4056-868b-225b7e440b0f)

The Program, uses a `PasswordHasher` and an `Alert` to pass arguments to a `CoreEncrypter`.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b8b57c8f-8f84-4675-90c8-28fccc939124)

Further down we have some hardcoded static strings:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bb20f0ca-450d-46f3-8884-2111cebc4517)

We need to figure out some parameter values in order to create a decryptor. We have `email1` and `email2` as they were hardcoded. Howeveer, Alert is created with the first argument being a `Program.UID`:   
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/53f20e29-908b-425c-a870-095faa30122d)

Which is generated randomly:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4d7660c7-b4b0-420f-9022-4ae5b8acef22)

Good news is that according to the Alert code, we already have this information.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ffde4105-e1ca-41aa-a8d3-a07b09d1da7b)

It's the ID we found already populated in the ransom note:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3e322ddd-6fa7-461b-afbe-7fd5f4151ac7)

The `Program.UID` is also used as the first argument for the `passwordHasher` and the salt + alertName are hardcoded values. Email is blank:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f7796e53-7c97-4610-be2c-24482e7aa46b)

Let's try to grab/steal some code and make a Decryptor. I've created a new project in Visual Studio and copied the Alert and PasswordHasher:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4921633a-27ad-44f3-81c4-07fae7c22119)

Then I wrote this Program do get a file as an argument and we can start decrypting files:  
```C#
using DecrypterApp;
using Encrypter.Class;
using System.Security.Cryptography;

if (args.Length != 1)
{
    Console.WriteLine("Usage: DecrypterApp <encrypted_file>");
    return;
}
Alert alert = new Alert("5K7X7E6X7V2D6F", "fraycrypter@korp.com", "fraydecryptsp@korp.com");
string encryptedFile = args[0];
PasswordHasher passwordHasher = new PasswordHasher();
string password = passwordHasher.GetHashCode("5K7X7E6X7V2D6F", "0f5264038205edfb1ac05fbb0e8c5e94"); 
string validatedAlert = alert.ValidateAlert(); 
string alertName = "ULTIMATUM"; 
string email = ""; 

CoreDecrypter decrypter = new CoreDecrypter(password, validatedAlert, alertName, email);
decrypter.DecryptFile(encryptedFile);

namespace DecrypterApp
{
    class CoreDecrypter
    {
        private string password;
        private string alert;
        private string alertName;
        private string email;

        public CoreDecrypter(string password, string validatedAlert, string alertName, string email)
        {
            this.password = password;
            this.alert = validatedAlert;
            this.alertName = alertName;
            this.email = email;
        }

        public void DecryptFile(string encryptedFile)
        {
            byte[] salt = new byte[]
            {
                0, 1, 1, 0, 1, 1, 0, 0
            };
            Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(password, salt, 4953);
            RijndaelManaged rijndaelManaged = new RijndaelManaged();
            rijndaelManaged.Key = rfc2898DeriveBytes.GetBytes(rijndaelManaged.KeySize / 8);
            rijndaelManaged.Mode = CipherMode.CBC;
            rijndaelManaged.Padding = PaddingMode.ISO10126;
            rijndaelManaged.IV = rfc2898DeriveBytes.GetBytes(rijndaelManaged.BlockSize / 8);

            string decryptedFilePath = encryptedFile.Substring(0, encryptedFile.Length - 5); // Remove ".korp" extension
            using (FileStream encryptedFileStream = new FileStream(encryptedFile, FileMode.Open))
            using (FileStream decryptedFileStream = new FileStream(decryptedFilePath, FileMode.Create))
            using (CryptoStream cryptoStream = new CryptoStream(encryptedFileStream, rijndaelManaged.CreateDecryptor(), CryptoStreamMode.Read))
            {
                cryptoStream.CopyTo(decryptedFileStream);
            }

            Console.WriteLine("File decrypted successfully.");
        }
    }
}
```
The directory specified by the challenge description contains only 1 .korp file so we can start with that one.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ac217d0d-79f5-4d43-b198-ac4bc3a30553)

We successfully decrypted the file and got a functional Excel in return which we can open and actually get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4b2e3bfa-b9f9-4bb7-b275-b58c62a97bb8)

This was a hard challenge worthy of the name. Once I thought of the quarantine, the name of the challenge made sense and I knew I was on the right track. Overall, it was a well designed challenge that made complete sense from start to finish, it was realistic and enjoyable to crack.

`HTB{2_f34r_1s_4_ch01ce_322720914448bf9831435690c5835634}`


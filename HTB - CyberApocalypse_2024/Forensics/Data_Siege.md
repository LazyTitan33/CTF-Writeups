# Data Siege

## Enumeration
We get a wireshark capture and have a look at `Statistics` -> `Protocol Hierarchy` and see some data:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/77b3e951-f645-40b7-8dae-00c93edebccf)

Following TCP stream, we see at stream 1 something about Java and springframework:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0881cb86-4b98-4212-940d-65b8f99ac140)

Continuing to follow the stream, we find a Powershell command having downloaded a weird executable file.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/db11ebee-d523-45e0-ab3f-487b87183311)

Luckily we've captured that file too so we can simply export it from the capture to look at later:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e6db4b84-e1b5-4081-8916-f73ca7571027)

TCP Stream 5 contains a lot of Base64 strings, some shorter, some longer. They can't be decoded to plaintext so they must be encrypted.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/57fb433f-6f1d-4fa9-8ff4-3b647435f450)

Further down we also find another powershell command with a Base64 encoded payload:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6ab77327-96b9-49b1-9b7e-585659bc1bad)

## Solution
Decoding the Powershell command, we find the 3rd part of the flag. Interesting. We're starting from the end, sure.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/99e00ccf-1a65-4de8-a99b-c4a1116cef61)

The Executable file is thankfully a .Net binary which makes it easier to analyse.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/44a05af2-bfe3-4b8d-be9e-c0e8a7cee4dd)

We see the program having a Decrypt function which will be handy for decryptying the Base64 blobs, I'm sure:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/739140db-d8f5-4216-9827-2ed356b26110)

We can also find a hardcoded encryptKey.. nice:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d1dc4efb-3f43-4dd4-a693-7787f82e0539)

Hippity-hoppity, your code is now my property. I don't want to run their code/executable so I made my own. I've grabbed their decryption code, modified it a little to be able to pass arguments to it and got this code which I compiled into an executable:  

```C#

using System.Security.Cryptography;
using System.Text;

namespace DecryptApp
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("Usage: DecryptApp <cipher_text>");
                return;
            }

            string cipherText = args[0];
            string decryptedText = Decrypt(cipherText);
            Console.WriteLine("Decrypted text: " + decryptedText);
        }

        public static string Decrypt(string cipherText)
        {
            string result;
            try
            {
                string encryptKey = "VYAemVeO3zUDTL6N62kVA";
                byte[] array = Convert.FromBase64String(cipherText);
                using (Aes aes = Aes.Create())
                {
                    Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(encryptKey, new byte[]
                    {
                        86,
                        101,
                        114,
                        121,
                        95,
                        83,
                        51,
                        99,
                        114,
                        51,
                        116,
                        95,
                        83
                    });
                    aes.Key = rfc2898DeriveBytes.GetBytes(32);
                    aes.IV = rfc2898DeriveBytes.GetBytes(16);
                    using (MemoryStream memoryStream = new MemoryStream())
                    {
                        using (CryptoStream cryptoStream = new CryptoStream(memoryStream, aes.CreateDecryptor(), CryptoStreamMode.Write))
                        {
                            cryptoStream.Write(array, 0, array.Length);
                            cryptoStream.Close();
                        }
                        cipherText = Encoding.Default.GetString(memoryStream.ToArray());
                    }
                }
                result = cipherText;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine("Cipher Text: " + cipherText);
                result = "error";
            }
            return result;
        }
    }
}
```

I started passing those base64 strings to my program and soon enough, found the 1st part of the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/674877d1-b127-45aa-9d12-1a6883ec9a6a)

Some decrypted base64 strings later, I also find part 2:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/71ae66af-4366-4ff3-a167-e8e661a9aafc)

`HTB{c0mmun1c4710n5_h45_b33n_r3570r3d_1n_7h3_h34dqu4r73r5}`

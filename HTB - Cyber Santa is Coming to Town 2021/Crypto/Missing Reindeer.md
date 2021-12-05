
![image](https://user-images.githubusercontent.com/80063008/144765824-ba7da162-36d3-495a-a5f7-8e0f7886c042.png)


We get a message.eml file which contains an encrypted.enc file and a pubkey.der file

![image](https://user-images.githubusercontent.com/80063008/144765826-f89c8e54-f6d4-4f3b-90d2-9180bf87f2c3.png)


Saved those locally and then ran RsaCtfTool.py on it

```bash
./RsaCtfTool.py --publickey pubkey.der --uncipherfile secret.enc 
```

Unciphered data:
```
HEX : 0xa415e596f3e4a21c25003081894a080532af6ba4739145593a9695f886b146e5b865b3c46fd2c14cc19059d8a3491018ff10fe4d02bfad9cceee6735c2844e87f10ada2593acb6988315f2e760a65b15fea3b781937af3651fdedae68e1210c4ed3602d0d1bc94e1f054ad
INT (big endian) : 307968727924643589446817054356670587947811738257755826328391346771555909495309166997072951847162296442948717292181103911669692516081555431892296155634695866133360083497101472628760457860959909333788155352877056162451321677649740405158218026991156435780392109
INT (little endian) : 325322852408515827924680177664573471113206438368894095154748946216388495533407429128074259190964109468771287894216654896504526078759213214576415893088320551628507634445347416332262568586203743010212094388519639262170697695732520271131614082510566363490489764
STR : b'\xa4\x15\xe5\x96\xf3\xe4\xa2\x1c%\x000\x81\x89J\x08\x052\xafk\xa4s\x91EY:\x96\x95\xf8\x86\xb1F\xe5\xb8e\xb3\xc4o\xd2\xc1L\xc1\x90Y\xd8\xa3I\x10\x18\xff\x10\xfeM\x02\xbf\xad\x9c\xce\xeeg5\xc2\x84N\x87\xf1\n\xda%\x93\xac\xb6\x98\x83\x15\xf2\xe7`\xa6[\x15\xfe\xa3\xb7\x81\x93z\xf3e\x1f\xde\xda\xe6\x8e\x12\x10\xc4\xed6\x02\xd0\xd1\xbc\x94\xe1\xf0T\xad'
```
That is not readable so that must mean there is another layer of encryption.

The first time I ran the files to the tool, I hadn't base64 decrypted the secret message.
![image](https://user-images.githubusercontent.com/80063008/144765880-63a90512-cb1b-4b85-aa3d-5b0a9a473632.png)

Used cat to read the original message, base64 decrypted it, sent the output to another file and ran that through the tool which eventually outputted the flag.
```bash
cat secret.enc|base64 -d > flag.enc
```

```bash
./RsaCtfTool.py --publickey pubkey.der --uncipherfile flag.enc
```
![image](https://user-images.githubusercontent.com/80063008/144765885-4d51dcff-4227-45cc-924d-d5a7d146b924.png)


HTB{w34k_3xp0n3n7_ffc896}


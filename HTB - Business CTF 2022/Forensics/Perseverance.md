For this challenge we get the following four files.

![image](https://user-images.githubusercontent.com/80063008/179469636-430babb8-2522-4e2a-891f-814a5ec88eca.png)

I wasn't sure what to do with them at the beginning so I started googling.

![image](https://user-images.githubusercontent.com/80063008/179469820-bb6f8681-07da-4cc0-a13a-03cb835cf0c5.png)

The first result points to this article with some details. This ended up getting me the tool I needed to parse through these files.

https://netsecninja.github.io/dfir-notes/wmi-forensics/

```bash
git clone https://github.com/mandiant/flare-wmi
cd flare-wmi/python-cim
virtualenv -p /usr/bin/python3.10 venv3
source venv3/bin/activate
pip install -r requirements
python3 setup.py install
```
I ran the tool with ../../ because I had the files two folders back from where I was.

```bash
python3 samples/show_filtertoconsumerbindings.py win7 ../../
```
And we can see a powershell command with an encoded base64 string.

![image](https://user-images.githubusercontent.com/80063008/179470081-bbcf89ad-b804-4526-b296-2641c8034b3b.png)

Decoding that, we can see it is pulling a property value from a specific class from the cimv2 namespace.

![image](https://user-images.githubusercontent.com/80063008/179470150-fd09157e-1396-4dec-9ff1-779b53dc2dbf.png)

We can use the same tool to carve out the class definitions and search for the Win32_MemoryArrayDevice class.

```bash
python3 samples/auto_carve_class_definitions.py ../../ 
```
And we see a long value of yet another base64 string.

![image](https://user-images.githubusercontent.com/80063008/179470364-ea87c6cd-d28c-4cc7-a135-74e30861c29e.png)

At first I base64 decoded it but got what looked like garbage to me. I first thought it might be encrypted but saw no signs of it. In fact, if you look closer at the first command, we see that it converts the base64 and then decompresses it. So this is something that's compressed.

Indeed, putting it through Cyberchef's magic recipe, we see that if we use Raw_Inflate after Base64 decoding it, we get a dll/exe file. The MZ header is our indicator for that.

![image](https://user-images.githubusercontent.com/80063008/179470803-e6e95623-a1e1-4083-8dbc-72f8f2806929.png)

Now instead of the Magic recipe, let's do this manually. First apply the Base64 recipe and then the Raw Inflate recipe and see what we can see in the strings of the file. Scrolling down I noticed a string terminating in equal signs, an usual indicator of Base64.

![image](https://user-images.githubusercontent.com/80063008/179470954-3b6dbcdc-2aa4-4692-9bc6-31cab8d07f60.png)

Because of the dots, I also applied the UTF-16LE decoder for Windows files and got the entire Base64 string.

![image](https://user-images.githubusercontent.com/80063008/179471115-025d9f2d-7f13-4039-8ff3-8f5c65d20638.png)

Decoding that we get the flag.

![image](https://user-images.githubusercontent.com/80063008/179471147-2dee2b8f-5129-434e-92d1-4d6df4428723.png)

HTB{1_th0ught_WM1_w4s_just_4_M4N4g3m3nt_T00l}

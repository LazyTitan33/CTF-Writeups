In this challenge, we are provided with a birthday_invite.docx file and a capture.pcapng file.

The first thing I did was to unzip the docx file and look through it. I found a base64 string that was stating to be part 2 of something.

![image](https://user-images.githubusercontent.com/80063008/179467180-f0b46cfe-e77e-474a-810e-04b1f04e44ff.png)

I decoded it to be part 2 of the flag.

![image](https://user-images.githubusercontent.com/80063008/179467347-5ee661d8-14d7-4ba5-9470-f9af88d8e148.png)

```bash
F0llina_h4s_
```

Not having much luck finding anything else within the docx files, I moved on to look through the pcap file. Opened it in Wireshark and started following TCP streams. I found an encoded powershell command being executed.

![image](https://user-images.githubusercontent.com/80063008/179467516-388f645a-c5f1-4398-ad9a-12e83a50a165.png)

Put this base64 string in powershell, used Decode Text to decode from UTFF-16LE because that's what Windows uses and got parts of another part of the flag.

![image](https://user-images.githubusercontent.com/80063008/179468028-527d1c11-1ab5-44f5-8cf7-694d053855ae.png)

To make things easier I put it in https://tio.run where you can run scripts in various languages, including powershell. We can see it's putting together the parts but it's missing some. We'll get back to that in a bit.

![image](https://user-images.githubusercontent.com/80063008/179468310-d906a7c6-dd81-4cda-88c8-3daf1e569efb.png)

```bash
b33n_pAtch
```
Looking some more through the Wireshark capture, under the protocol hierarchy, we can see some text data being transfered as well. 

![image](https://user-images.githubusercontent.com/80063008/179468632-81cb98cb-a2fe-4f1c-bd1c-2a8b53fb94ad.png)

We can use filter data-text-lines and can see a 200 OK. 

![image](https://user-images.githubusercontent.com/80063008/179468643-1526594b-c250-406c-98e4-6b7bc5a664b7.png)

We follow that and find a URL encoded string. I somehow missed this when looking through TCP requests.

![image](https://user-images.githubusercontent.com/80063008/179468694-e304afd2-0542-45b5-b8c3-5f9a87a8c6f3.png)

I put it through Cyberchef and decoded it. Further down, we see the expected Follina string. We knew this is what we were dealing with from the beginning.

![image](https://user-images.githubusercontent.com/80063008/179468799-a80fe994-f149-4dc6-b50a-9aee1aa1ccc2.png)

Decoding the base64 string we get part 1 of the flag.

![image](https://user-images.githubusercontent.com/80063008/179468846-f6beda1a-e507-4829-9b5d-73396989d3be.png)

```
HTB{Zer0_DayZ_4Re_C0Ol_BuT_
```

Now putting it all together, we get:

```bash
HTB{Zer0_DayZ_4Re_C0Ol_BuT_F0llina_h4s_b33n_pAtch
```

Obviously that's not the entire flag because the grammar isnt' correct and we don't have the squigly bracket at the end. So we are missing something. Going back to part 3, based on the grammar we know we need an ed or 3d and we do see it. The squigly line is also there with an exclamation mark.

![image](https://user-images.githubusercontent.com/80063008/179469133-038b446e-64d1-4512-a93f-0bfc0b84a536.png)

Putting it all together again we get the proper flag. I'm sure there are better ways to do it, but in the rush of a CTF, that's what I managed.

```bash
HTB{Zer0_DayZ_4Re_C0Ol_BuT_F0llina_h4s_b33n_pAtch3d!}
```


Running strings on the provided pcap file we can see a string that looks like a reversed base64.

![image](https://user-images.githubusercontent.com/80063008/198272330-0da311e8-bddb-4835-b44a-bd0cfe3f35a5.png)

Copied it, echoed it, reversed it and base64 decoded it within the terminal.

```bash
echo "==gC9FSI5tGMwA3cfRjd0o2Xz0GNjNjYfR3c1p2Xn5WMyBXNfRjd0o2eCRFS"|rev|base64 -d
```

![image](https://user-images.githubusercontent.com/80063008/198272437-c7bbd787-a20a-4fd4-969b-7f089d00ac4a.png)

HTB{j4v4_5pr1ng_just_b3c4m3_j4v4_sp00ky!!}
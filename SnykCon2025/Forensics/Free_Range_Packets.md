# Free Range Packets
![image](https://github.com/user-attachments/assets/63ae93ae-baa5-45f3-95f4-1a8552e83f42)

Attachment: [freeRangePackets.pcapng](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/freeRangePackets.pcapng)

## Writeup

Based on the challenge description, I knew I had to carve out the btl2cap field from the capture file. With tshark and some further grepping and cutting I can eventually cleanly get the flag out.

```bash
tshark -r freeRangePackets.pcapng -Y 'btl2cap.payload' -T fields -e btl2cap.payload 2>/dev/null|grep -v '09ff01065c'|cut -c 7-|cut -c 1-2|xxd -r -p
```

![image](https://github.com/user-attachments/assets/d65af82d-4199-45f5-baa1-e946bf8670d9)


flag{b5be72ab7e0254c056ffb57a0db124ce}

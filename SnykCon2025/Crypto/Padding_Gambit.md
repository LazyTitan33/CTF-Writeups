# Padding Gambit
![image](https://github.com/user-attachments/assets/1b079028-ef9f-4b0c-a571-5a34ec403851)

Attachment: [Padding_Gambit.7z](https://github.com/LazyTitan33/CTF-Writeups/raw/64fef7c6d09e2b125412107c9db92832f999f515/SnykCon2025/attachments/Padding_Gambit.7z)

## Writeup

When accessing the provided URL, I get this page where it's asking for a code.  

![image](https://github.com/user-attachments/assets/74fc4547-f142-453e-85d3-c236e252cdec)

The provided source code consists mainly of a server.js and a crypto.js as below:  

```javascript
const crypto = require('crypto')

class Crypto {
  constructor (key, algorithm = `aes-${key.length * 8}-cbc`) {
    this.key = key
    this.algorithm = algorithm
  }

  encrypt (iv, plain) {
    let cipher = crypto.createCipheriv(this.algorithm, this.key, iv)
    return Buffer.concat([cipher.update(plain), cipher.final()])
  }

  decrypt (iv, cipher) {
    let decipher = crypto.createDecipheriv(this.algorithm, this.key, iv)
    return Buffer.concat([decipher.update(cipher), decipher.final()])
  }
}

exports.Crypto = Crypto
```

According to the server.js, accessing the `/api/token` endpoint, it allows me to create an encrypted token:  

```javascript
app.get('/api/token', (req, res) => {
  const encryptedToken = encrypt(tokenCode);
  res.json({ token: encryptedToken });
});
```

Making a POST request on `/api/submit/:token` it decrypts the token and requires me to enter a valid `secretCode` to get the flag:  

```javascript
/**
 * Vulnerable endpoint that expects the token as part of the URL.
 * Example call: POST /api/submit/<encryptedToken>
 */
app.post('/api/submit/:token', (req, res, next) => {
  const urlToken = req.params.token;
  if (!urlToken) {
    return res.status(400).json({ error: 'Missing token in URL' });
  }

  const decryptionResult = decrypt(urlToken);
  if (!decryptionResult.success) {
    const err = new Error(`Decryption failed: ${decryptionResult.error}`);
    err.statusCode = 400;
    return next(err);
  }

  const submittedCode = req.body.code;
  if (!submittedCode) {
    return res.status(400).json({ error: 'Missing code in request body' });
  }

  if (submittedCode === secretCode) {
    res.json({ message: `Correct code! Flag: ${flag}` });
  } else {
    res.status(400).json({ error: 'Incorrect code' });
  }
});
```
This server has a potential padding oracle attack vulnerability due to how the decrypt function processes encrypted tokens and returns distinct error messages. Since AES-CBC is used, an attacker could exploit this behavior to systematically decrypt the token by observing the errors returned.

```javascript
function decrypt(base64UrlText) {
  try {
    // 1) URL-decode
    const base64Decoded = decodeURIComponent(base64UrlText);

    // 2) Convert from Base64 to a Buffer of raw bytes
    const combinedBuffer = Buffer.from(base64Decoded, 'base64');
    if (combinedBuffer.length < 16) {
      throw new Error('Combined buffer too short to contain IV + ciphertext');
    }

    // 3) IV is the first 16 bytes, ciphertext is the remainder
    const iv = combinedBuffer.slice(0, 16);
    const cipherBytes = combinedBuffer.slice(16);

    // 4) Decrypt
    const plainBuffer = crypt.decrypt(iv, cipherBytes);
    return { success: true, decrypted: plainBuffer.toString('utf8') };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

I used [padbuster](https://www.kali.org/tools/padbuster/) with the syntax below:  

```bash
padbuster 'http://challenge.ctf.games:31769/api/submit/lIi37VwofxGcSudiwg9%2FDP8Lrj4B17suDcY8%2B6ojgxKQmbsw8biJxrxhG4kOK4wF' \
'lIi37VwofxGcSudiwg9%2FDP8Lrj4B17suDcY8%2B6ojgxKQmbsw8biJxrxhG4kOK4wF' 16 -encoding 0 -proxy '127.0.0.1:8080' \
-post '{"code":"lazy"}' -headers 'Content-Type::application/json'
```
After some time, the `tokenCode` is decrypted:  

![image](https://github.com/user-attachments/assets/1491ac1e-8369-41eb-9516-4891c3488368)

```
pastebin.com/rzZMdkvs
```

Accessing the pastebin I get another piece of the puzzle.  

![image](https://github.com/user-attachments/assets/b9c4e737-0f5c-4530-b589-293819d12a31)

```
would you like to play a game? 1PPPP3/2P1P3/1P3PP1/1PPP1P2/1P3PP1/2PP2P1/2PP1P1P/2P1P2P w - - 0 1
```

I recognize this as being FEN notation for chess which makes sense given the images and challenge description. It can be mapped out on a chess board with multiple online resources, including this one: https://www.dcode.fr/fen-chess-notation

![image](https://github.com/user-attachments/assets/cb3e896b-494c-4359-bdce-fb08b8270115)

I stared at it for a while and then I got the idea to convert it to binary. Any occupied squares are 1 and any unoccupied ones are 0:

```
01111000 00101000 01000110 01110100 01000110 00110010 00110101 00101001
```
This converts to `x(FtF25)` which is a subtle reference to Snyk Fetch The Flag 2025, the name of the event. This is the secretCode I need to get the flag.

![image](https://github.com/user-attachments/assets/a91d32fe-90e3-42ce-b9c8-ec7fb7f82a62)


flag{311bdc6168aee1a66943ccd20986f30b}

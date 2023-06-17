# Blobber

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/acbb6411-5f63-4d37-8d2e-8ff163b98b6d)

The file we get is a SQLite database file:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fd082323-82cb-4741-b474-460bd923b595)

Opening it in the DB Browser, we notice a lot of entries with random looking names. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/85a8e2c0-6715-42d1-8170-b32152a50389)

It was all garbage. I spend some time trying to find the needle in the haystack but then I remembered it's a SQL database so we can simply use queries. All the `name` columns contained junk, and all the `data` columns were empty. But that is something we can double check using the SQL query below to list everything that doesn't have a NULL data column entry:

```sql
select * from blobber where data != 'NULL';
```
It turns out we have a blob in one of the entries:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ff21e91e-da27-4cb5-881e-4405945170c9)

Good thing I learned to leave assumptions at the door when doing CTFs. Now I used some short python scripting to pull out the blob and write it to a file since I didn't know exactly what it was.

```python3
import sqlite3

conn = sqlite3.connect('blobber')
cursor = conn.cursor()

cursor.execute("select data from blobber where data != 'NULL';")

result = cursor.fetchone()
blob_content = result[0]

with open('output.bin', 'wb') as file:
    file.write(blob_content)
    
conn.close()
```

We can use the file command on it and find out it's a `bzip2` archive.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/46ae663f-1a3f-4187-bd1a-c8a18ec4ce0a)

We can use `bzip2 -d` to decompress it:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a31c432a-8e87-4083-88a1-9352efc3fc42)

And the resulting file is a picture:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/287040cc-ed2d-4945-a5d1-5106a6b96d01)

That contains our flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/949327a5-ce65-4895-bd2f-6384857dbd00)

flag{b93a6292f3491c8e2f6cdb3addb5f588}

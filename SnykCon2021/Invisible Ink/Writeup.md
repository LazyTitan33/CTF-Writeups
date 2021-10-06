# Invisible Ink


Main page shows:

![image](https://user-images.githubusercontent.com/80063008/136173120-074b9ccc-8caa-48ce-912e-98ffa7c33ef2.png)


We are given a package.json and a index.js file.

The package.json file shows a vulnerable lodash version. This can be found out either by googling each version of the dependencies mentioned, or by running the Snyk tool.

![image](https://user-images.githubusercontent.com/80063008/136173152-eb98730e-ea9e-4d74-a1df-e0105dc69f68.png)

It is vulnerable to Prototype Pollution: https://snyk.io/vuln/SNYK-JS-LODASH-73638: CVE-2018-16487

This is the code in the index.js

```javascript
    1 	'use strict';
    2 	
    3 	const fs = require('fs');
    4 	const express = require('express');
    5 	const app = express();
    6 	const bodyParser = require('body-parser');
    7 	const _ = require('lodash');
    8 	
    9 	const options = {};
   10 	const flag = fs.readFileSync('./flag', 'utf-8').trim();
   11 	const docHtml = fs.readFileSync('./index.html', 'utf-8');
   12 	
   13 	app.use(bodyParser.json());
   14 	
   15 	app.get('/', (req, res) => {
   16 	    res.send(docHtml);
   17 	});
   18 	
   19 	app.post('/echo', (req, res) => {
   20 	    const out = {
   21 	        userID: req.headers['x-forwarded-for'] || req.connection.remoteAddress,
   22 	        time: Date.now()
   23 	    };
   24 	
   25 	    _.merge(out, req.body);
   26 	
   27 	    if (options.flag) {
   28 	        out.flag = flag;
   29 	    } else {
   30 	        out.flag = 'disabled';
   31 	    }
   32 	
   33 	    res.json(out);
   34 	    process.exit(0);
   35 	});
   36 	
   37 	app.listen(8000);
```

This researcher has an example POC for this CVE.

https://github.com/Kirill89/prototype-pollution-explained

Doing the normal POST as described and required by the index.js script and the mainpage. We can see that the flag is currently disabled.
![image](https://user-images.githubusercontent.com/80063008/136173238-147cb514-6c90-406f-8eff-4efecaf33f4a.png)

Then doing the prototype pollution to enable the flag:
![image](https://user-images.githubusercontent.com/80063008/136173282-c3b0073b-a2ee-4cfb-8397-7d4710a8a8d8.png)


SNYK{6a6a6fff87f3cfdca056a077804838d4e87f25f6a11e09627062c06f142b10dd}


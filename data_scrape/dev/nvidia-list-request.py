import requests
import json

url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"

payload = json.dumps({
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
})
headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

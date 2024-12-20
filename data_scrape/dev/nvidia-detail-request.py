import requests

url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/job/China-Shanghai/Web-Application-Software-Engineer---New-College-Graduate-2025_JR1992495"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

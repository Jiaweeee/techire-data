import requests
import json

url = "https://jobs.bytedance.com/api/v1/search/job/posts"

payload = json.dumps({
  "keyword": "",
  "limit": 100,
  "offset": 0,
  "job_category_id_list": [],
  "tag_id_list": [],
  "location_code_list": [],
  "subject_id_list": [],
  "recruitment_id_list": [],
  "portal_type": 4,
  "job_function_id_list": [],
  "storefront_id_list": [],
  "portal_entrance": 1
})
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'Cookie': 'ttwid=1%7Cxi4SHVMU6EbQHMkfs7jqRyMaWwHVPcdjqymb0_bv6x4%7C7C1718762270%7C7C697820f0ffae633f25913bf0c2367c9c7bb426fcf88fee2364a34c1063b961; locale=en-US; channel=overseas; platform=pc; s_v_web_id=verify_m4e4144n_dfGBiQVi_xGL0_4Vdm_8zT7_nyl08fyHn221; device-id=74456391446691249669; tea_uid=7445639144687322630',
  'Dnt': '1',
  'Env': 'undefined',
  'Host': 'jobs.bytedance.com',
  'Origin': 'https://jobs.bytedance.com',
  'Portal-Channel': 'overseas',
  'Portal-Platform': 'pc',
  'Referer': 'https://jobs.bytedance.com/en/position',
  'Sec-Ch-Ua': '"Chromium";v="131", "Not_A_Brand";v="24"',
  'Sec-Ch-Ua-Mobile': '?0',
  'Sec-Ch-Ua-Platform': '"macOS"',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# 移除 'Accept-Encoding' 头，这样服务器就会返回未压缩的内容
headers.pop('Accept-Encoding', None)

response = requests.request("POST", url, headers=headers, data=payload)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Raw Response:", response.text)

if response.status_code == 200:
    try:
        print("JSON Response:", response.json())
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

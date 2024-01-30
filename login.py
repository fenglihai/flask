import requests, json
url = "https://10.16.96.15:10081/platformapi/auth/sso/verify/code"

payload = '{\"loginType\":\"USERNAME\",\"loginTab\":\"PWD_TAB\",\"verifyCodeType\":\"SMS\",\"captchaCode\":\"f2m2\",\"randomStr\":\"w8ikl8nd\",\"domain\":\"http://ceshi.com\",\"appCode\":\"DD_UNIFIED_BASIC\",\"password\":\"8H56rQ9S/6I7bbXu\",\"account\":\"3nJ6pwZU\"}'
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/json;charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'Origin': 'https://10.16.96.15:10081',
  'Connection': 'keep-alive',
  'Referer': 'https://10.16.96.15:10081/',
  'Cookie': 'null=null',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)

print(response.text)
import requests

url = "https://site.infobric.com"

session = requests.Session()

response = session.get(url)

print("Initial:", response.status_code)

print(session.cookies)

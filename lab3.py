import http.client
import json
import urllib.parse

conn = http.client.HTTPConnection("167.172.172.227:8000")
#1.	Отправить HTTP запрос GET /number/{Вариант}. 
# В ответе будет выдано число – сохранить и вывести его в консоль.
conn.request('GET', '/number/7', )
r2 = conn.getresponse().read().decode()
r2_json = json.loads(r2)
print(r2_json['number'])


#2.	Отправить HTTP запрос GET /number/ с параметром запроса option={Вариант}. 
# В ответе будут выданы число и операция. 
conn.request('GET', '/number/?option=7', )
r1 = conn.getresponse().read().decode()
r1_json = json.loads(r1)
print(r1_json['number'])

p = r1_json['number'] + r2_json['number']

print(p)

#Отправить HTTP запрос POST /number/ с телом option={Вариант}. 
#В заголовках необходимо указать content-type=application/x-www-form-urlencoded. 
#В ответе будут выданы число и операция. headers = {'Content-type': 'application/x-www-form-urlencoded'}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn.request('POST', '/number/', 'option=7', headers)
response = conn.getresponse().read().decode()
response_json = json.loads(response)
print(response_json['number'])
d = p + response_json['number']
print(d)

#4.	Отправить HTTP запрос PUT /number/ с телом JSON {"option": {Вариант}}. 
# В заголовках необходимо указать content-type=application/json. 
# В ответе будут выданы число и операция. 
headers = {'Content-type': 'application/json'}
body = json.dumps({'option': 7})
conn.request('PUT', '/number/', body, headers)
response = conn.getresponse().read().decode()
response_json = json.loads(response)
print(response_json['number'])
print(response)
v = (d * (response_json['number']))
print(v)


#5.	Отправить HTTP запрос DELETE /number/ с телом JSON {"option": {Вариант}}. 
# В ответе будут выданы число и операция. 
body = json.dumps({'option': 7})
conn.request('DELETE', '/number/', body)
response = conn.getresponse().read().decode()
response_json = json.loads(response)
print(response_json['number'])
print(response)
print((response_json['number']) / v)
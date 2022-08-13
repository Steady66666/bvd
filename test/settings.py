import json
# f = open('settings.json','r').read()
f = json.load(open('settings.json','r'))
user_name = f['user_name']
password = f['password']
# print(password)
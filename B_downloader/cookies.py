import json
f = json.load(open('cookies.json','r'))

cookies = f['cookies']
if f['cookies'] != {}:
    dedeuserid = cookies['DedeUserID']
import json
f = json.load(open('cookies.json','r'))
# print(f)
cookies = f['cookies']
dedeuserid = cookies['DedeUserID']
# print(dedeuserid)
# cookies={'b_timer': '%7B%22ffp%22%3A%7B%22333.130.fp.risk_4196BCAD%22%3A%221828DE4E428%22%2C%22333.1193.fp.risk_4196BCAD%22%3A%221828DE582C9%22%2C%22333.1007.fp.risk_4196BCAD%22%3A%221828DE58912%22%7D%7D', 'innersign': '0', 'sid': '6v9dnh8r', 'DedeUserID': '470586328', 'i-wanna-go-back': '-1', 'bili_jct': '89c124eb04ff83982d9d9baaec44f752', 'SESSDATA': '00ec8343%2C1675790006%2C1f182%2A81', 'buvid_fp': '6a3dc367b91ee78539cee335334c9edc', 'b_nut': '1660237964', 'fingerprint': '6a3dc367b91ee78539cee335334c9edc', 'buvid4': 'CC3BF89B-D98E-87ED-CFDA-8435B184285366005-022081201-4f+PGJDMABp0yPm5BG5O/Q%3D%3D', '_uuid': 'B924CDFC-77C10-5728-864D-5DD2BD23835D63942infoc', 'buvid3': '4196BCAD-0D04-C8C4-B1BC-96AA8882C64966005infoc', 'DedeUserID__ckMd5': '1cf619a1493eec8d', 'b_ut': '5', 'b_lsid': 'F1FBAB79_1828DE4E29F'}
# print(type(cookies))
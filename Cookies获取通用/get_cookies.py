
from urllib.parse import unquote
from urllib.parse import quote
import requests,json,qrcode,os,re
from flask import Flask,request,render_template,send_file

header = {'origin':'https://www.bilibili.com','referer':'https://www.bilibili.com','user-agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}

app = Flask(import_name=__name__)

def get_qr():
    url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
    res = requests.get(url=url,headers=header).json()['data']
    res = str(res).replace('\'','\"')
    with open('get_qr.json','w')as f:
        f.write(res)
        f.close()
    # return res

@app.route('/', methods=["GET"])
def index():
    res = get_qr()
    with open('get_qr.json','r')as f:
        res = json.loads(f.read())
    f.close()
    qrurl = res['url']
    qrurl = quote(str(qrurl))
    qrurl = f'/qr?url={qrurl}'
    print(qrurl)
    return render_template('index.html',qrurl = qrurl)

@app.route('/qr',methods=["GET"])
def qr():
    b_url = request.values.get('url')
    print(b_url)
    image = qrcode.make(b_url)
    image.save('image.png')
    print(os.getcwd())
    return send_file(f'image.png')

@app.route('/login',methods=["GET"])
def login():

    with open('get_qr.json','r')as f:
        res = json.loads(f.read())
    f.close()
    oauthKey = res['oauthKey']
    url2 = f'http://passport.bilibili.com/qrcode/getLoginInfo?oauthKey={oauthKey}'
    # print(oauthKey)
    requests_json = {"oauthKey":oauthKey,"gourl":"http://www.bilibili.com"}
    cookie_before = requests.post(url=url2,json=requests_json,headers=header).json()
    print(cookie_before)
    if cookie_before['code'] == 0:
        data = cookie_before['data']['url']
        DedeUserID = re.findall('DedeUserID=(.*?)&',data)[0]
        DedeUserID__ckMd5 = re.findall('DedeUserID__ckMd5=(.*?)&',data)[0]
        SESSDATA = re.findall('SESSDATA=(.*?)&',data)[0]
        bili_jct = re.findall('bili_jct=(.*?)&',data)[0]
        cookie = f'{{\"cookies\":{{\"DedeUserID\":\"{DedeUserID}\",\"DedeUserID__ckMd5\":\"{DedeUserID__ckMd5}\",\"SESSDATA\":\"{SESSDATA}\",\"bili_jct\":\"{bili_jct}\"}}}}'
        with open('cookies.json','w')as f:
            f.write(cookie)
        f.close()
        return send_file('cookies.json',as_attachment=True,attachment_filename='cookies.json')

    

'''
url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
header = {'origin':'https://www.bilibili.com','referer':'https://www.bilibili.com','user-agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}
res = requests.get(url=url,headers=header).json()['data']
oauthKey = res['oauthKey']
qrurl = res['url']
qr_image = qrcode.make(qrurl)
qr_image.save('qr.png')
# print(qrurl)


url2 = 'http://passport.bilibili.com/qrcode/getLoginInfo'
requests_json = {
    "oauthKey":oauthKey,
    "gourl":"http://www.bilibili.com"
}
res = requests.post(url=url2,json=requests_json,headers=header).json()
print(res)
'''
if __name__== '__main__':
    app.run(debug=False,port = 9876,host='0.0.0.0')
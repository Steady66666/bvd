# B站专属请求模块
import requests,time
from cookies import cookies

def get_response(url):
    requests.adapters.DEFAULT_RETRIES = 5
    headers ={'origin':'https://www.bilibili.com','referer':'https://www.bilibili.com','user-agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}
    try:
        response  = requests.get(url=url,headers=headers,cookies=cookies,stream=True,timeout=20)
    except requests.exceptions.ConnectTimeout:
        print('无效链接，响应超时，请重新请求')
        time.sleep(3)
        exit(1)
    except:
        print('未知网络错误，请重新请求')
        exit(1)
    return response 